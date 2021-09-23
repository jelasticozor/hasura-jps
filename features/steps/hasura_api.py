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


@given(u'she has added a todo through the following graphql mutation')
def step_impl(context):
    mutation = context.text
    response, _ = context.graphql_client.execute(
        query=mutation, run_as_admin=False)
    context.current_todo_id = response['data']['insert_todos_one']['id']


@given(u'the user has applied the database migrations of the \'{project_name}\'')
def step_impl(context, project_name):
    context.path_to_hasura_project = os.path.join(
        context.hasura_projects_folder, project_name
    )
    success = context.hasura_client.apply_migrations(
        context.path_to_hasura_project)
    assert success is True


@given(u'the user has started the todo with the hasura action')
def step_impl(context):
    mutation = context.text
    response, _ = context.graphql_client.execute(
        query=mutation, run_as_admin=False)
    assert 'errors' not in response


@given(u'the \'hasura-action\' function has been deployed on the faas engine')
def step_impl(context):
    function_name = 'hasura-action'
    context.faas_client.login()
    context.current_faas_function = function_name
    hasura_node_ip = context.current_env_info.get_node_ips(node_group='cp')
    exit_code = context.faas_client.deploy(
        function_name,
        env={
            'GRAPHQL_ENDPOINT': f'http://{hasura_node_ip}/v1/graphql'
        })
    assert exit_code == 0


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
    variables = {
        'id': context.current_todo_id
    }
    response, _ = context.graphql_client.execute(
        query=query, variables=variables, run_as_admin=False)
    print('response = ', response)
    context.actual_todo = response['data']['todos_by_pk']


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
    actual_description = context.actual_todo['description']
    assert expected_description == actual_description


@then(u'she gets state \'{expected_state}\'')
@then(u'state \'{expected_state}\'')
def step_impl(context, expected_state):
    actual_state = context.actual_todo['state']
    assert expected_state == actual_state
