(function () {
  'use strict';

  function initTheme() {
    const themeToggles = document.querySelectorAll('#theme-toggle, .subpage-theme-toggle');
    if (themeToggles.length === 0) return;

    function updateThemeIcons(theme) {
      themeToggles.forEach((btn) => {
        const sun = btn.querySelector('.sun-icon');
        const moon = btn.querySelector('.moon-icon');
        if (theme === 'light') {
          if (sun) sun.classList.add('active');
          if (moon) moon.classList.remove('active');
        } else {
          if (moon) moon.classList.add('active');
          if (sun) sun.classList.remove('active');
        }
      });
    }

    const isMobileOrTablet = window.innerWidth <= 1024;
    const deviceKey = isMobileOrTablet ? 'style_ui_theme_mobile' : 'style_ui_theme_desktop';
    let activeTheme = document.documentElement.getAttribute('data-theme');

    try {
      const savedTheme = localStorage.getItem(deviceKey);
      if (savedTheme) {
        activeTheme = savedTheme;
      } else if (!activeTheme) {
        activeTheme = isMobileOrTablet ? 'light' : 'dark';
      }
    } catch (e) {
      if (!activeTheme) activeTheme = isMobileOrTablet ? 'light' : 'dark';
    }

    document.documentElement.setAttribute('data-theme', activeTheme);
    updateThemeIcons(activeTheme);

    themeToggles.forEach((btn) => {
      btn.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', nextTheme);
        try {
          localStorage.setItem(deviceKey, nextTheme);
        } catch (e) {}

        updateThemeIcons(nextTheme);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();
