# Privacy

Style UI is a static site. It has no accounts, no cookies, and no analytics.

## Local storage

The theme toggle stores the selected theme in the browser:

- `style_ui_theme_mobile`
- `style_ui_theme_desktop`

These keys stay on the visitor's device. They are not sent to a server.

## Third-party requests

The current site loads resources from:

- Google Fonts for the typeface.
- jsDelivr for the GSAP scripts. The Lenis scroll library is served from this repository.
- image.thum.io when a preview image is missing.
- Google favicon service when a logo is missing.

These services receive the visitor's IP address and request headers as part of the request. Style UI does not control their data practices. Read the privacy policy of each provider for details.

## Data collection

Style UI does not collect names, email addresses, or account data. It does not sell or share visitor data.

If analytics or click counts are added later, this document will be updated before the feature ships.

## Contact

For a privacy question, open an issue at https://github.com/miqdadbadjuber/style-ui/issues.
