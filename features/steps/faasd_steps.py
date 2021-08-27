import os

from features.utils.faas_client import FaasClient
from features.utils.sockets import can_open_socket
from features.utils.timing import wait_until


@given(u'the faas engine is installed')
def step_impl(context):
    context.jps_client.install(
        context.serverless_manifest, context.current_env_name)


@when(u'a user logs on the faas engine')
def step_impl(context):
    faas_node_type = 'docker'
    faas_node_group = 'faas'
    env_info = context.control_client.get_env_info(context.current_env_name)
    faas_node_ip = env_info.get_node_ips(
        node_type=faas_node_type, node_group=faas_node_group)[0]
    secrets_folder = '/var/lib/faasd/secrets'
    username = context.file_client.read(
        context.current_env_name, os.path.join(secrets_folder, 'basic-auth-user'), node_type=faas_node_type,
        node_group=faas_node_group)
    password = context.file_client.read(
        context.current_env_name, os.path.join(secrets_folder, 'basic-auth-password'), node_type=faas_node_type,
        node_group=faas_node_group)
    faas_client = FaasClient(gateway_url=faas_node_ip,
                             gateway_port=context.faas_port)
    # TODO: this should part of another step responsible for waiting until the port is available
    try:
        wait_until(lambda: can_open_socket(faas_node_ip, context.faas_port),
                   timeout_in_sec=120, period_in_sec=5)
    except TimeoutError:
        context.exit_code = 1
    context.exit_code = faas_client.login(username, password)


@then(u'she gets a success response')
def step_impl(context):
    assert context.exit_code == 0
