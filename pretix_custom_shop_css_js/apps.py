from django.utils.translation import gettext_lazy as _
from pretix.base.plugins import PluginConfig, PLUGIN_LEVEL_ORGANIZER
from . import __version__


class PluginApp(PluginConfig):
    default = True
    name = 'pretix_custom_shop_css_js'
    verbose_name = _('Custom Shop CSS/JS')

    class PretixPluginMeta:
        name = _('Custom Shop CSS/JS')
        author = 'Fraktvred'
        description = _('Inject custom CSS and JavaScript into all presale pages for an organizer.')
        visible = True
        version = __version__
        category = 'CUSTOMIZATION'
        compatibility = 'pretix>=4.0.0'
        level = PLUGIN_LEVEL_ORGANIZER

    def ready(self):
        from . import signals  # NOQA
