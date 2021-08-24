@given(u'the faas engine is installed')
def step_impl(context):
    context.jps_client.install(
        context.serverless_manifest, context.current_env_name)


@when(u'a user logs on the faas engine')
def step_impl(context):
    faas_node_type = 'ubuntu-vps'
    env_info = context.control_client.get_env_info(context.current_env_name)
    faas_node_ip = env_info.get_node_ips(node_type=faas_node_type)[0]
    username = context.file_client.read(
        context.current_env_name, '/var/lib/faasd/secrets/basic-auth-user', node_type=faas_node_type)
    password = context.file_client.read(
        context.current_env_name, '/var/lib/faasd/secrets/basic-auth-password', node_type=faas_node_type)
    print('username = ', username)
    print('password = ', password)
    # TODO:
    # 4. call faas-cli login -g http://node-ip:8080 --username <username> --password <password>
    # --> returns 1 if failed


@then(u'she gets a success response')
def step_impl(context):
    # TODO: verify that the faas-cli return success
    raise NotImplementedError(u'STEP: Then she gets a success response')
