@then(u'the current Jelastic version is {expected_version}')
def step_impl(context, expected_version):
    actual_version = context.jps_client.get_engine_version()
    assert expected_version == actual_version
