from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm


class CustomCodeForm(SettingsForm):
    custom_css = forms.CharField(
        label=_('Custom CSS'),
        widget=forms.Textarea(attrs={'rows': 12, 'class': 'form-control', 'style': 'font-family: monospace;'}),
        required=False,
        help_text=_('CSS injected into the <head> of every presale page for this organizer.'),
    )
    custom_js = forms.CharField(
        label=_('Custom JavaScript'),
        widget=forms.Textarea(attrs={'rows': 12, 'class': 'form-control', 'style': 'font-family: monospace;'}),
        required=False,
        help_text=_('JavaScript injected before </body> on every presale page for this organizer.'),
    )
