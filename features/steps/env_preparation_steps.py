@given(u'a jelastic environment with a node of type \'{node_type}\' is available')
def step_impl(context, node_type):
    print('node_type = ', node_type)
    raise NotImplementedError(
        u'STEP: Given a jelastic environment with a node of type \'ubuntu-vps\' is available')
