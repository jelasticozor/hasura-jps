import os

from test_utils.manifest_data import get_manifest_data

from features.utils.graphql_client import GraphQLClient


@given(u'the user has installed the main manifest')
def step_impl(context):
    success_text = context.jps_client.install_from_file(
        context.main_manifest, context.current_env_name)
    context.current_env_info = context.control_client.get_env_info(
        context.current_env_name)
    assert context.current_env_info.is_running()
    cp_node_ip = context.current_env_info.get_node_ips(node_group='cp')[0]
    external_api_endpoint = f'http://{context.current_env_info.domain()}/v1/graphql'
    internal_api_endpoint = f'http://{cp_node_ip}:{context.hasura_internal_port}'
    context.manifest_data = get_manifest_data(success_text)
    hasura_admin_secret = context.manifest_data['Hasura Admin Secret']
    context.hasura_client = context.hasura_client_factory.create(
        internal_api_endpoint, hasura_admin_secret)
    context.graphql_client = GraphQLClient(
        external_api_endpoint, hasura_admin_secret)


@given(u'its database metadata')
def step_impl(context):
    success = context.hasura_client.apply_metadata(
        context.path_to_hasura_project)
    assert success is True


@given(u'she adds a todo through the following graphql mutation')
def step_impl(context):
    mutation = context.text
    response, _ = context.graphql_client.execute(
        query=mutation, run_as_admin=False)
    print('response = ', response)
    context.new_todo_id = response['data']['insert_todos_one']['id']


@given(u'the user has applied the database migrations of the \'{project_name}\'')
def step_impl(context, project_name):
    context.path_to_hasura_project = os.path.join(
        context.hasura_projects_folder, project_name
    )
    success = context.hasura_client.apply_migrations(
        context.path_to_hasura_project)
    assert success is True


@when(u'the user applies the database migrations of the \'{project_name}\'')
def step_impl(context, project_name):
    context.path_to_hasura_project = os.path.join(
        context.hasura_projects_folder, project_name
    )
    context.success = context.hasura_client.apply_migrations(
        context.path_to_hasura_project)


@when(u'she retrieves the new todo with the following query')
def step_impl(context):
    query = context.text
    response, _ = context.graphql_client.execute(query=query, run_as_admin=False)
    context.actual_description = response['data']['todos_by_pk']['description']


@then(u'there is {nb_nodes:d} {node_type} node in the {node_group} node group')
@then(u'there are {nb_nodes:d} {node_type} nodes in the {node_group} node group')
def step_impl(context, nb_nodes, node_type, node_group):
    node_ips = context.current_env_info.get_node_ips(
        node_group=node_group, node_type=node_type)
    assert len(node_ips) == nb_nodes


@then(u'she gets success')
def step_impl(context):
    assert context.success is True


@then(u'she gets the description')
def step_impl(context):
    expected_description = context.text
    assert expected_description == context.actual_description
