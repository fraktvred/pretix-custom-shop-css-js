import hashlib

from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import View
from pretix.base.models import Organizer
from pretix.control.views.organizer import OrganizerSettingsFormView
from .forms import CustomCodeForm


class CustomCodeSettingsView(OrganizerSettingsFormView):
    form_class = CustomCodeForm
    template_name = 'pretix_custom_shop_css_js/settings.html'

    def get_success_url(self):
        return reverse('plugins:pretix_custom_shop_css_js:settings', kwargs={
            'organizer': self.request.organizer.slug,
        })


def _content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()[:8]


class CustomCSSView(View):
    def get(self, request, organizer, **kwargs):
        try:
            org = Organizer.objects.get(slug=organizer)
        except Organizer.DoesNotExist:
            raise Http404
        css = org.settings.custom_css or ''
        if not css:
            raise Http404
        response = HttpResponse(css, content_type='text/css; charset=utf-8')
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        response['ETag'] = f'"{_content_hash(css)}"'
        return response


class CustomJSView(View):
    def get(self, request, organizer, **kwargs):
        try:
            org = Organizer.objects.get(slug=organizer)
        except Organizer.DoesNotExist:
            raise Http404
        js = org.settings.custom_js or ''
        if not js:
            raise Http404
        response = HttpResponse(js, content_type='application/javascript; charset=utf-8')
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        response['ETag'] = f'"{_content_hash(js)}"'
        return response
