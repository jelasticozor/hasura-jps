import os

import requests
from behave import *
from softozor_test_utils.sockets import host_has_port_open
from test_utils.manifest_data import get_manifest_data

from features.utils.faas import deploy


@given(
    u'a jelastic environment with an ubuntu-git docker node')
def step_impl(context):
    path_to_manifest = os.path.join(
        context.test_manifests_folder, f'faas.yml')
    success_text = context.jps_client.install_from_file(
        path_to_manifest,
        context.current_env_name)
    context.manifest_data = get_manifest_data(success_text)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert context.current_env_info.is_running()


@given(u'the faas engine is installed')
def step_impl(context):
    context.jps_client.install_from_file(
        context.serverless_manifest, context.current_env_name, settings={
            'authApiKey': 'the-fake-api-key',
            'authUrl': 'the-fake-auth-url'
        })
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    faas_node_type = 'docker'
    faas_node_group = 'faas'
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
        faas_node_ip, username, password)


@given(u'the \'hello-python\' function has been deployed on the faas engine')
def step_impl(context):
    function_name = 'hello-python'
    context.faas_client.login()
    context.current_faas_function = function_name
    deployment_success = deploy(
        context.faas_client, context.path_to_serverless_configuration, function_name)
    assert deployment_success is True


@given(u'a user is logged on the faas engine')
def step_impl(context):
    exit_code = context.faas_client.login()
    assert exit_code == 0


@when(u'a user logs on the faas engine')
def step_impl(context):
    context.exit_code = context.faas_client.login()


@when(u'she deploys the \'{function_name}\' function to the faas engine')
def step_impl(context, function_name):
    context.exit_code = not deploy(
        context.faas_client, context.path_to_serverless_configuration, function_name)
    context.current_faas_function = function_name


@when(u'a user invokes it with payload \'{function_payload}\'')
def step_impl(context, function_payload):
    rq = requests.post(f'http://{context.faas_client.endpoint}/function/{context.current_faas_function}',
                       data=function_payload)
    context.current_function_http_status = rq.status_code
    context.current_function_response_content = rq.text


@then(u'she gets a success response')
def step_impl(context):
    assert context.exit_code == 0


@then(u'she gets http status {http_status:d}')
def step_impl(context, http_status):
    assert context.current_function_http_status == http_status


@then(u'she gets content')
def step_impl(context):
    expected_content = context.text
    assert context.current_function_response_content == expected_content, \
        f'expected {expected_content}, got {context.current_function_response_content}'
