from behave import *


@then('the \'{manifest_field}\' is the current Jelastic user email')
def step_impl(context, manifest_field):
    actual_email = context.manifest_data[manifest_field]
    account_client = context.jelastic_clients_factory.create_account_client()
    user_info = account_client.get_user_info()
    expected_email = user_info.email()
    assert expected_email == actual_email


@then('the \'{manifest_field}\' contains {field_length} characters')
def step_impl(context, manifest_field, field_length):
    actual_field_value = context.manifest_data[manifest_field]
    assert len(actual_field_value) == field_length
