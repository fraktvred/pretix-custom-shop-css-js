def test_form_valid_with_empty_fields(organizer):
    from pretix_custom_shop_css_js.forms import CustomCodeForm
    form = CustomCodeForm(data={'custom_css': '', 'custom_js': ''}, obj=organizer)
    assert form.is_valid()


def test_form_valid_with_css_and_js(organizer):
    from pretix_custom_shop_css_js.forms import CustomCodeForm
    form = CustomCodeForm(
        data={'custom_css': 'body {}', 'custom_js': 'alert(1)'},
        obj=organizer,
    )
    assert form.is_valid()
    assert form.cleaned_data['custom_css'] == 'body {}'
    assert form.cleaned_data['custom_js'] == 'alert(1)'
