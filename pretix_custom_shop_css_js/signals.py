import hashlib

from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pretix.presale.signals import global_html_footer, global_html_head
from pretix.control.signals import nav_organizer


def _content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()[:8]


@receiver(global_html_head, dispatch_uid='pretix_custom_shop_css_js_head')
def inject_css(sender, request=None, **kwargs):
    if not request or not hasattr(request, 'organizer'):
        return ''
    css = request.organizer.settings.custom_css or ''
    if not css:
        return ''
    url = reverse('plugins:pretix_custom_shop_css_js:css', kwargs={'organizer': request.organizer.slug})
    return f'<link rel="stylesheet" href="{url}?v={_content_hash(css)}">'


@receiver(global_html_footer, dispatch_uid='pretix_custom_shop_css_js_footer')
def inject_js(sender, request=None, **kwargs):
    if not request or not hasattr(request, 'organizer'):
        return ''
    js = request.organizer.settings.custom_js or ''
    if not js:
        return ''
    url = reverse('plugins:pretix_custom_shop_css_js:js', kwargs={'organizer': request.organizer.slug})
    return f'<script src="{url}?v={_content_hash(js)}"></script>'


@receiver(nav_organizer, dispatch_uid='pretix_custom_shop_css_js_nav')
def nav_organizer_link(sender, request=None, **kwargs):
    from django.urls import resolve, reverse
    url = resolve(request.path_info)
    return [{
        'label': _('Custom CSS/JS'),
        'url': reverse('plugins:pretix_custom_shop_css_js:settings', kwargs={
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_custom_shop_css_js',
        'icon': 'code',
        'parent': reverse('control:organizer.edit', kwargs={
            'organizer': request.organizer.slug,
        }),
    }]
