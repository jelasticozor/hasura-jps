import os

import requests
from test_utils.manifest_data import get_manifest_data

from features.utils.manifest import get_base_url_from_manifest_content
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
        context.fusionauth_manifest, context.current_env_name)


@when(u'a user installs the fusionauth manifest with kick-starting')
def step_impl(context):
    with open(context.fusionauth_manifest) as file:
        manifest_content = file.read()
        base_url = get_base_url_from_manifest_content(manifest_content)
        context.jps_client.install(
            manifest_content, context.current_env_name, settings={
                'kickstartJson': f'{base_url}/features/data/fusionauth/kickstart.json'
            })
    current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert current_env_info.is_running()
    context.current_fusionauth_url = current_env_info.get_node_url_from_name(
        'auth')


def fusionauth_is_up(fusionauth_url, timeout_in_sec=300, period_in_sec=5):
    def test_is_up():
        response = requests.get(f'{fusionauth_url}/api/status')
        return response.status_code == 200
    try:
        wait_until(lambda: test_is_up(),
                   timeout_in_sec=timeout_in_sec, period_in_sec=period_in_sec)
        return True
    except TimeoutError:
        return False


@then(u'fusionauth is up and running')
def step_impl(context):
    assert fusionauth_is_up(context.current_fusionauth_url) is True
