from features.utils.faas_client import FaasClient
from features.utils.sockets import can_open_socket
from features.utils.timing import wait_until

faas_node_type = 'docker'
faas_node_group = 'faas'


def host_has_port_open(host, port, timeout_in_sec=120, period_in_sec=5):
    try:
        wait_until(lambda: can_open_socket(host, port),
                   timeout_in_sec=timeout_in_sec, period_in_sec=period_in_sec)
        return True
    except TimeoutError:
        return False


@given(u'the faas engine is installed')
def step_impl(context):
    context.jps_client.install(
        context.serverless_manifest, context.current_env_name)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    faas_node_ip = context.current_env_info.get_node_ips(
        node_type=faas_node_type, node_group=faas_node_group)[0]
    assert host_has_port_open(faas_node_ip, context.faas_port)


@when(u'a user logs on the faas engine')
def step_impl(context):
    faas_node_ip = context.current_env_info.get_node_ips(
        node_type=faas_node_type, node_group=faas_node_group)[0]
    username = context.file_client.read(
        context.current_env_name,
        '/var/lib/faasd/secrets/basic-auth-user',
        node_type=faas_node_type,
        node_group=faas_node_group)
    password = context.file_client.read(
        context.current_env_name,
        '/var/lib/faasd/secrets/basic-auth-password',
        node_type=faas_node_type,
        node_group=faas_node_group)
    faas_client = FaasClient(
        gateway_url=faas_node_ip,
        gateway_port=context.faas_port)
    context.exit_code = faas_client.login(username, password)


@then(u'she gets a success response')
def step_impl(context):
    assert context.exit_code == 0
