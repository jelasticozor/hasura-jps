import os

import requests
from test_utils.manifest_data import get_manifest_data

from features.utils.timing import wait_until


@given(u'a jelastic environment with a database and fusionauth')
def step_impl(context):
    path_to_manifest = os.path.join(
        context.test_manifests_folder, f'fusionauth.yml')
    success_text = context.jps_client.install_from_file(
        path_to_manifest,
        context.current_env_name)
    context.manifest_data = get_manifest_data(success_text)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)


@when(u'a user installs the fusionauth manifest without kick-starting')
def step_impl(context):
    context.jps_client.install_from_file(
        context.fusionauth_manifest, context.current_env_name, settings={
            'databaseName': context.manifest_data['Auth Database Name'],
            'databaseRootUsername': context.manifest_data['Database Admin User'],
            'databaseRootPassword': context.manifest_data['Database Admin Password'],
            'databaseUsername': context.manifest_data['Auth Database Username'],
            'databasePassword': context.manifest_data['Auth Database Password']
        })
    current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert current_env_info.is_running()
    context.current_fusionauth_ip = current_env_info.get_node_ips(
        node_group='auth', node_type='docker')[0]


@when(u'a user installs the fusionauth manifest with kick-starting')
def step_impl(context):
    context.jps_client.install_from_file(
        context.fusionauth_manifest, context.current_env_name, settings={
            'databaseName': context.manifest_data['Auth Database Name'],
            'databaseRootUsername': context.manifest_data['Database Admin User'],
            'databaseRootPassword': context.manifest_data['Database Admin Password'],
            'databaseUsername': context.manifest_data['Auth Database Username'],
            'databasePassword': context.manifest_data['Auth Database Password'],
            'kickstartJson': f'{context.base_url}/features/data/fusionauth/kickstart.json'
        })
    current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert current_env_info.is_running()
    context.current_fusionauth_ip = current_env_info.get_node_ips(
        node_group='auth', node_type='docker')[0]


def fusionauth_is_up(fusionauth_ip, fusionauth_port, timeout_in_sec=300, period_in_sec=15):
    def test_is_up():
        try:
            response = requests.get(
                f'http://{fusionauth_ip}:{fusionauth_port}/api/status')
            return response.status_code == 200
        except:
            return False

    try:
        wait_until(lambda: test_is_up(),
                   timeout_in_sec=timeout_in_sec, period_in_sec=period_in_sec)
        return True
    except TimeoutError:
        return False


@then(u'fusionauth is up and running')
def step_impl(context):
    assert fusionauth_is_up(context.current_fusionauth_ip,
                            context.fusionauth_port) is True
