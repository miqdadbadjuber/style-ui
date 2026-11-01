# Contributing to Style UI

Style UI is a static directory. Contributions that keep the site fast, readable, and easy to maintain are welcome.

## Ways to contribute

- Submit a tool through the [submission issue form](https://github.com/miqdadbadjuber/style-ui/issues/new?template=submit-tool.yml).
- Report a broken link or a bug with the [bug report form](https://github.com/miqdadbadjuber/style-ui/issues/new?template=bug-report.yml).
- Propose a feature with the [feature request form](https://github.com/miqdadbadjuber/style-ui/issues/new?template=feature-request.yml).
- Improve documentation or send a pull request for a small fix.

## Before you start

Open an issue before starting a large change. This is especially important for layout, animation, and visual changes, because the current design is intentional and should not shift without agreement.

Small fixes, such as a typo, a broken link, or a missing `alt` attribute, can go straight to a pull request.

## Local setup

The site has no package dependencies and no build step.

```bash
git clone https://github.com/miqdadbadjuber/style-ui.git
cd style-ui
npx serve .
```

You can also use any static server:

```bash
python -m http.server 8080
```

Open the URL printed by the server.

## Adding or updating a tool

1. Check the relevant category page and confirm the tool is not already listed.
2. Add or edit the card in the category page HTML. Keep the existing card structure and `data-*` attributes.
3. Update the tab count for the category when the number of entries changes.
4. Add the logo to `assets/logos` and the preview to `assets/previews`. Use a square logo and a wide screenshot.
5. Add clear `alt` text to every new image.
6. Test the page in light and dark mode, at mobile and desktop widths.
7. Confirm that the new outbound URL works.
8. Run `npm run validate`. It checks that every referenced asset exists, the tab counts match the cards, image sizes stay under 300 KB, and links use https.

If the tool is submitted through an issue, the maintainer will handle the card and assets.

## Code style

- Use vanilla HTML, CSS, and JavaScript. Do not add a framework or a runtime dependency for a small feature.
- Reuse existing classes, CSS variables, and component patterns before adding new ones.
- Keep new JavaScript in `assets/js`. The only exception is the small theme script in each page head, which has to run before paint to avoid a flash of the wrong theme.
- Do not add inline event handlers in new code. Use `addEventListener` instead.
- Use WebP for new preview images when the source allows it.
- Keep image files under 300 KB. Compress before committing.
- Do not commit local backups, scratch files, or editor settings.

## Pull request checklist

- [ ] The change is limited to one topic.
- [ ] I tested the change in light and dark themes.
- [ ] I tested the change at mobile, tablet, and desktop widths.
- [ ] I updated the tab count if I added or removed a tool.
- [ ] I added or updated `alt` text for images.
- [ ] New images are compressed and under 300 KB.
- [ ] New links return a valid page.
- [ ] `npm run validate` passes.
- [ ] I did not commit local backups or tooling files.

## Commit messages

Use a short prefix that describes the change:

- `feat:` for a new feature or tool entry
- `fix:` for a bug fix
- `docs:` for documentation
- `perf:` for a performance change
- `chore:` for maintenance

Example: `feat: add Aceternity UI to the component directory`

## Review

The maintainer reviews pull requests and may ask for changes to keep the catalog consistent. Visual changes need prior discussion. Security reports should follow [SECURITY.md](SECURITY.md), not a public pull request.

## Questions

Join the [Discord server](https://discord.gg/VWKggJfHFR) for quick questions, or open an issue with the feature request form if you are unsure where a change belongs.
