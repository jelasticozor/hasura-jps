import os

import requests
from test_utils.manifest_data import get_manifest_data

from features.utils.timing import wait_until


def hasura_is_available(endpoint):
    def predicate():
        response = requests.get(f'{endpoint}/v1/version')
        return response.status_code == 200

    try:
        wait_until(lambda: predicate(), timeout_in_sec=30, period_in_sec=0.5)
        return True
    except TimeoutError:
        return False


@given(u'the user has installed the main manifest')
def step_impl(context):
    success_text = context.jps_client.install_from_file(
        context.main_manifest, context.current_env_name)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert context.current_env_info.is_running()
    cp_node_ip = context.current_env_info.get_node_ips(node_group='cp')[0]
    # hasura_endpoint = f'http://{context.current_env_info.domain()}'
    hasura_endpoint = f'http://{cp_node_ip}:8080'
    context.manifest_data = get_manifest_data(success_text)
    hasura_admin_secret = context.manifest_data['Hasura Admin Secret']
    context.hasura_client = context.hasura_client_factory.create(
        hasura_endpoint, hasura_admin_secret)
    assert hasura_is_available(hasura_endpoint) is True


@when(u'the user applies the database migrations of the \'{project_name}\'')
def step_impl(context, project_name):
    path_to_project = os.path.join(
        context.hasura_projects_folder, project_name
    )
    context.success = context.hasura_client.apply_migrations(path_to_project)


@then(u'there is {nb_nodes:d} {node_type} node in the {node_group} node group')
@then(u'there are {nb_nodes:d} {node_type} nodes in the {node_group} node group')
def step_impl(context, nb_nodes, node_type, node_group):
    node_ips = context.current_env_info.get_node_ips(
        node_group=node_group, node_type=node_type)
    assert len(node_ips) == nb_nodes


@then(u'she gets success')
def step_impl(context):
    assert context.success is True
