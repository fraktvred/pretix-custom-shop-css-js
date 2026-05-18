import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def admin_user(db):
    from pretix.base.models import User
    return User.objects.create_superuser('admin@example.com', 'adminpassword')


@pytest.fixture
def logged_in_client(admin_user):
    client = Client()
    client.login(email='admin@example.com', password='adminpassword')
    return client


@pytest.fixture
def organizer_with_team(organizer, admin_user):
    from pretix.base.models import Team
    team = Team.objects.create(organizer=organizer, name='Admins', all_organizer_permissions=True, all_events=True)
    team.members.add(admin_user)
    return organizer


def test_settings_page_get(logged_in_client, organizer_with_team):
    url = reverse('plugins:pretix_custom_shop_css_js:settings', kwargs={'organizer': organizer_with_team.slug})
    response = logged_in_client.get(url)
    assert response.status_code == 200


def test_settings_page_saves_css_and_js(logged_in_client, organizer_with_team):
    from pretix.base.models import Organizer
    url = reverse('plugins:pretix_custom_shop_css_js:settings', kwargs={'organizer': organizer_with_team.slug})
    response = logged_in_client.post(url, {
        'custom_css': 'body { background: blue; }',
        'custom_js': 'console.log("test");',
    })
    assert response.status_code in (200, 302)
    fresh = Organizer.objects.get(pk=organizer_with_team.pk)
    assert fresh.settings.custom_css == 'body { background: blue; }'
    assert fresh.settings.custom_js == 'console.log("test");'


def test_settings_page_clears_values(logged_in_client, organizer_with_team):
    from pretix.base.models import Organizer
    organizer_with_team.settings.set('custom_css', 'body {}')
    url = reverse('plugins:pretix_custom_shop_css_js:settings', kwargs={'organizer': organizer_with_team.slug})
    logged_in_client.post(url, {'custom_css': '', 'custom_js': ''})
    fresh = Organizer.objects.get(pk=organizer_with_team.pk)
    assert (fresh.settings.custom_css or '') == ''


def test_css_serve_view_returns_css(client, organizer):
    organizer.settings.custom_css = 'body { color: red; }'
    url = reverse('plugins:pretix_custom_shop_css_js:css', kwargs={'organizer': organizer.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert 'text/css' in response['Content-Type']
    assert response.content == b'body { color: red; }'
    assert 'immutable' in response['Cache-Control']


def test_css_serve_view_404_when_empty(client, organizer):
    organizer.settings.custom_css = ''
    url = reverse('plugins:pretix_custom_shop_css_js:css', kwargs={'organizer': organizer.slug})
    response = client.get(url)
    assert response.status_code == 404


def test_js_serve_view_returns_js(client, organizer):
    organizer.settings.custom_js = 'console.log(1);'
    url = reverse('plugins:pretix_custom_shop_css_js:js', kwargs={'organizer': organizer.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert 'javascript' in response['Content-Type']
    assert response.content == b'console.log(1);'
    assert 'immutable' in response['Cache-Control']


def test_js_serve_view_404_when_empty(client, organizer):
    organizer.settings.custom_js = ''
    url = reverse('plugins:pretix_custom_shop_css_js:js', kwargs={'organizer': organizer.slug})
    response = client.get(url)
    assert response.status_code == 404


def test_css_etag_changes_with_content(client, organizer):
    organizer.settings.custom_css = 'body { color: red; }'
    url = reverse('plugins:pretix_custom_shop_css_js:css', kwargs={'organizer': organizer.slug})
    etag1 = client.get(url)['ETag']
    organizer.settings.custom_css = 'body { color: blue; }'
    etag2 = client.get(url)['ETag']
    assert etag1 != etag2
