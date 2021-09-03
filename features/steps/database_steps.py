@given(u'the database is installed')
def step_impl(context):
    context.jps_client.install_from_file(
        context.database_manifest, context.current_env_name)
    env_info = context.control_client.get_env_info(context.current_env_name)
    context.primary_node_ip = env_info.get_node_ip_from_name('Primary')
    context.secondary_node_ip = env_info.get_node_ip_from_name('Secondary')
    # TODO: get password from success text (get it from the installation of the root manifest)
    # TODO: create postgres connection to both
