from behave import *


@then(u'the current Jelastic version is {expected_version}')
def step_impl(context, expected_version):
    jps_client = context.jelastic_clients_factory.create_jps_client()
    actual_version = jps_client.get_engine_version()
    assert expected_version == actual_version
