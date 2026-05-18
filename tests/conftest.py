import pytest


@pytest.fixture
def organizer(db):
    from pretix.base.models import Organizer
    return Organizer.objects.create(name='Test Org', slug='testorg')
