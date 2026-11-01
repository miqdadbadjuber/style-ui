#!/usr/bin/env node
// Static checks for the Style UI catalog. Run with: node scripts/validate.js

const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const PAGES = [
  "index.html",
  "ui-components/index.html",
  "background-generator/index.html",
  "design-md/index.html",
];
const HTML_PAGES = [...PAGES, "404.html"];
const VALID_STATUS = new Set(["Free", "Paid", "Semi-free"]);
const IMAGE_BUDGET_BYTES = 300 * 1024;
const REQUIRED_FILES = [
  "index.html",
  "404.html",
  "README.md",
  "LICENSE",
  "CONTRIBUTING.md",
  "CODE_OF_CONDUCT.md",
  "SECURITY.md",
  "PRIVACY.md",
  "ROADMAP.md",
  "robots.txt",
  "sitemap.xml",
  "site.webmanifest",
  "vercel.json",
];

const errors = [];
const warnings = [];
const fail = (message) => errors.push(message);
const warn = (message) => warnings.push(message);

function read(relativePath) {
  return fs.readFileSync(path.join(ROOT, relativePath), "utf8");
}

for (const file of REQUIRED_FILES) {
  if (!fs.existsSync(path.join(ROOT, file))) fail(`missing required file: ${file}`);
}

// Local asset references resolve. The pattern captures any scheme or leading
// slash so absolute URLs are skipped and root-relative paths use the repo root.
const assetPattern = /(?:https?:\/\/[^\s"'<>]+)?(?:\.\.\/|\/)?assets\/[A-Za-z0-9._/-]+\.(?:png|jpe?g|webp|svg|ico|css|js)/g;
const sourceFiles = [
  ...HTML_PAGES,
  "README.md",
  "site.webmanifest",
  ...fs.readdirSync(path.join(ROOT, "assets/css")).map((name) => `assets/css/${name}`),
  ...fs.readdirSync(path.join(ROOT, "assets/js")).map((name) => `assets/js/${name}`),
];

for (const file of sourceFiles) {
  const text = read(file);
  const seen = new Set();
  for (const match of text.match(assetPattern) || []) {
    if (seen.has(match)) continue;
    seen.add(match);
    if (/^https?:\/\//.test(match)) continue;
    const resolved = match.startsWith("/")
      ? path.join(ROOT, match.slice(1))
      : path.resolve(ROOT, path.dirname(file), match);
    if (!fs.existsSync(resolved)) {
      fail(`${file}: referenced asset does not exist -> ${match}`);
      continue;
    }
    if (/\.(png|jpe?g|webp)$/i.test(resolved)) {
      const size = fs.statSync(resolved).size;
      if (size > IMAGE_BUDGET_BYTES) {
        fail(`${file}: image over 300 KB (${Math.round(size / 1024)} KB) -> ${match}`);
      }
    }
  }
}

// Root-relative links in HTML must point at a real file.
const rootRefPattern = /(?:href|src)="(\/[^"#?]+\.(?:png|jpe?g|webp|svg|ico|css|js|xml|txt|webmanifest))"/g;
for (const page of HTML_PAGES) {
  for (const match of read(page).matchAll(rootRefPattern)) {
    if (!fs.existsSync(path.join(ROOT, match[1].slice(1)))) {
      fail(`${page}: root-relative link does not exist -> ${match[1]}`);
    }
  }
}

// Card data on each catalog page.
for (const page of PAGES) {
  const text = read(page);
  const cards = text.match(/<a\b[^>]*class="g4-card"[^>]*>/g) || [];
  const hasTabs = /class="t-tab"/.test(text);
  const counts = new Map();
  const urls = new Map();

  for (const tag of cards) {
    const status = (tag.match(/data-status="([^"]*)"/) || [])[1];
    const name = (tag.match(/data-name="([^"]*)"/) || [])[1];
    const href = (tag.match(/href="([^"]*)"/) || [])[1];

    if (hasTabs) {
      if (!status || !VALID_STATUS.has(status)) {
        fail(`${page}: card with invalid data-status "${status}" (${name || href || "unnamed"})`);
      } else {
        counts.set(status, (counts.get(status) || 0) + 1);
      }
      if (!name) fail(`${page}: card missing data-name (${href || "unnamed"})`);
    }

    if (href) {
      if (urls.has(href)) fail(`${page}: duplicate tool URL ${href}`);
      urls.set(href, true);
      if (href.startsWith("http://")) fail(`${page}: insecure link ${href}`);
    }
  }

  // Tab badges must match the cards actually on the page.
  const tabPattern = /<button[^>]*class="t-tab"[^>]*data-filter="([^"]+)"[^>]*>[\s\S]*?<span class="tab-badge">(\d+)<\/span>/g;
  let tabMatch;
  let badgeTotal = 0;
  while ((tabMatch = tabPattern.exec(text)) !== null) {
    const filter = tabMatch[1];
    const badge = Number(tabMatch[2]);
    if (filter === "all") {
      badgeTotal = badge;
    } else {
      const actual = counts.get(filter) || 0;
      if (badge !== actual) {
        fail(`${page}: "${filter}" tab badge says ${badge}, page has ${actual}`);
      }
    }
  }
  if (hasTabs && badgeTotal !== cards.length) {
    fail(`${page}: "All" tab badge says ${badgeTotal}, page has ${cards.length} cards`);
  }

  if (cards.length === 0) warn(`${page}: no tool cards found`);
}

// Accessibility basics on catalog images.
for (const page of HTML_PAGES) {
  const text = read(page);
  const imgs = text.match(/<img\b[^>]*>/g) || [];
  for (const img of imgs) {
    if (!/\balt="/.test(img)) fail(`${page}: <img> without alt -> ${img.slice(0, 90)}`);
  }
}

// Em dashes are banned in this project.
const EM_DASH = "—";
const COPY_FILES = [...HTML_PAGES, "README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md", "PRIVACY.md", "CODE_OF_CONDUCT.md"];
for (const file of COPY_FILES) {
  if (read(file).includes(EM_DASH)) fail(`${file}: contains an em dash`);
}

for (const message of warnings) console.warn(`warn  ${message}`);
for (const message of errors) console.error(`error ${message}`);

if (errors.length > 0) {
  console.error(`\n${errors.length} problem(s) found.`);
  process.exit(1);
}

console.log(`All checks passed. ${warnings.length} warning(s).`);
