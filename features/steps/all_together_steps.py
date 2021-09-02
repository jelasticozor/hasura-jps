@when(u'a user installs the main manifest')
def step_impl(context):
    context.jps_client.install(context.main_manifest, context.current_env_name)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)


@then(u'there is {nb_nodes:d} single {node_type} node in the {node_group} node group')
def step_impl(context, nb_nodes, node_type, node_group):
    node_ips = context.current_env_info.get_node_ips(
        node_group=node_group, node_type=node_type)
    assert len(node_ips) == 1
