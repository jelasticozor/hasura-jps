import requests

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
    context.faas_client = context.faas_client_factory.create(
        context.faas_node_ip, username, password)


@given(u'the \'{function_name}\' function has been deployed on the faas engine')
def step_impl(context, function_name):
    context.faas_client.login()
    context.current_faas_function = function_name
    exit_code = context.faas_client.deploy(function_name)
    assert exit_code == 0


@given(u'a user is logged on the faas engine')
def step_impl(context):
    exit_code = context.faas_client.login()
    assert exit_code == 0


@when(u'a user logs on the faas engine')
def step_impl(context):
    context.exit_code = context.faas_client.login()


@when(u'a user deploys the \'{function_name}\' function to the faas engine')
def step_impl(context, function_name):
    context.exit_code = context.faas_client.deploy(function_name)
    context.current_faas_function = function_name


@when(u'a user invokes it with payload \'{function_payload}\'')
def step_impl(context, function_payload):
    rq = requests.post(f'{context.faas_client.endpoint}/function/{context.current_faas_function}',
                       data=function_payload)
    context.current_function_http_status = rq.status_code
    context.current_function_response_content = rq.text


@then(u'she gets a success response')
def step_impl(context):
    assert context.exit_code == 0


@then(u'she gets http status {http_status}')
def step_impl(context, http_status):
    assert context.current_function_http_status == http_status


@then(u'she gets content')
def step_impl(context):
    expected_content = context.text
    assert context.current_function_response_content == expected_content
