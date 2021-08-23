@given(u'the faas engine is installed on the node of type \'{node_type}\'')
@when(u'the faas engine gets installed on the node of type \'{node_type}\'')
def step_impl(context, node_type):
    print('node_type = ', node_type)
    raise NotImplementedError(
        u'STEP: Given the faas engine is installed on the node of type \'ubuntu-vps\'')


@when(u'a user logs on the faas engine')
def step_impl(context):
    raise NotImplementedError(u'STEP: When a user logs on the faas engine')


@then(u'the installation is successful')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the installation is successful')


@then(u'she gets a success response')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then she gets a success response')
