from django.urls import re_path
from .views import CustomCodeSettingsView, CustomCSSView, CustomJSView

urlpatterns = [
    re_path(
        r'^control/organizer/(?P<organizer>[^/]+)/custom-css-js/$',
        CustomCodeSettingsView.as_view(),
        name='settings',
    ),
    re_path(
        r'^(?P<organizer>[^/]+)/custom-css-js/css\.css$',
        CustomCSSView.as_view(),
        name='css',
    ),
    re_path(
        r'^(?P<organizer>[^/]+)/custom-css-js/js\.js$',
        CustomJSView.as_view(),
        name='js',
    ),
]
