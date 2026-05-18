# pretix-custom-shop-css-js

A [pretix](https://pretix.eu) plugin that lets organizer admins inject custom CSS and JavaScript into all presale pages — including the organizer event listing and individual event pages.

## Features

- Per-organizer CSS and JS, configurable via the pretix control panel
- Injected on every presale page (event listing + event pages)
- No server access required — edit via the admin UI

## Installation

```bash
pip install pretix-custom-shop-css-js
```

Add `pretix_custom_shop_css_js` to `INSTALLED_APPS` in your pretix config, or install and enable via the pretix plugin manager.

## Usage

1. Install the plugin and restart pretix
2. In the control panel, navigate to your organizer
3. Go to **Plugins** and enable **Custom Shop CSS/JS**
4. A new **Custom CSS/JS** entry will appear in the organizer sidebar
5. Paste your CSS and/or JavaScript and click **Save**

The code is injected on every presale page for that organizer (CSS in `<head>`, JS before `</body>`).

## Development

```bash
git clone https://github.com/fraktvred/pretix-custom-shop-css-js
cd pretix-custom-shop-css-js
pip install -e .
pytest
```

## License

Apache Software License 2.0
