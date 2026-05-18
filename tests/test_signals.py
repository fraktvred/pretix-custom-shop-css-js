import hashlib
from unittest.mock import MagicMock, patch


def make_request(organizer=None):
    request = MagicMock()
    if organizer is not None:
        request.organizer = organizer
    else:
        del request.organizer
    return request


def _hash(content):
    return hashlib.md5(content.encode()).hexdigest()[:8]


def test_inject_css_returns_link_tag(organizer):
    organizer.settings.custom_css = 'body { color: red; }'
    from pretix_custom_shop_css_js.signals import inject_css
    request = make_request(organizer)
    with patch('pretix_custom_shop_css_js.signals.reverse', return_value='/testorg/custom-css-js/css.css'):
        result = inject_css(sender=None, request=request)
    h = _hash('body { color: red; }')
    assert result == f'<link rel="stylesheet" href="/testorg/custom-css-js/css.css?v={h}">'


def test_inject_css_empty_setting_returns_empty_string(organizer):
    organizer.settings.custom_css = ''
    from pretix_custom_shop_css_js.signals import inject_css
    request = make_request(organizer)
    result = inject_css(sender=None, request=request)
    assert result == ''


def test_inject_css_no_organizer_on_request_returns_empty_string():
    from pretix_custom_shop_css_js.signals import inject_css
    request = make_request(organizer=None)
    result = inject_css(sender=None, request=request)
    assert result == ''


def test_inject_js_returns_script_tag(organizer):
    organizer.settings.custom_js = 'console.log("hello");'
    from pretix_custom_shop_css_js.signals import inject_js
    request = make_request(organizer)
    with patch('pretix_custom_shop_css_js.signals.reverse', return_value='/testorg/custom-css-js/js.js'):
        result = inject_js(sender=None, request=request)
    h = _hash('console.log("hello");')
    assert result == f'<script src="/testorg/custom-css-js/js.js?v={h}"></script>'


def test_inject_js_empty_setting_returns_empty_string(organizer):
    organizer.settings.custom_js = ''
    from pretix_custom_shop_css_js.signals import inject_js
    request = make_request(organizer)
    result = inject_js(sender=None, request=request)
    assert result == ''


def test_inject_js_no_organizer_on_request_returns_empty_string():
    from pretix_custom_shop_css_js.signals import inject_js
    request = make_request(organizer=None)
    result = inject_js(sender=None, request=request)
    assert result == ''


def test_different_css_content_produces_different_hash(organizer):
    from pretix_custom_shop_css_js.signals import inject_css
    organizer.settings.custom_css = 'body { color: red; }'
    request = make_request(organizer)
    with patch('pretix_custom_shop_css_js.signals.reverse', return_value='/testorg/custom-css-js/css.css'):
        result1 = inject_css(sender=None, request=request)
    organizer.settings.custom_css = 'body { color: blue; }'
    with patch('pretix_custom_shop_css_js.signals.reverse', return_value='/testorg/custom-css-js/css.css'):
        result2 = inject_css(sender=None, request=request)
    assert result1 != result2
