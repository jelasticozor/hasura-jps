import psycopg2


@given(u'the database is installed')
def step_impl(context):
    assert 'Username' in context.manifest_data
    assert 'Password' in context.manifest_data
    admin_user = context.manifest_data['Username']
    admin_password = context.manifest_data['Password']
    context.jps_client.install_from_file(
        context.database_manifest, context.current_env_name, settings={
            "adminUsername": admin_user,
            "adminPassword": admin_password,
            "databaseName": context.database_name,
            "username": context.database_user,
            "password": context.database_password
        })
    env_info = context.control_client.get_env_info(context.current_env_name)
    primary_node_ip = env_info.get_node_ip_from_name('Primary')
    assert primary_node_ip is not None
    secondary_node_ip = env_info.get_node_ip_from_name('Secondary')
    assert secondary_node_ip is not None
    context.primary_connection = psycopg2.connect(host=primary_node_ip,
                                                  user=admin_user,
                                                  password=admin_password,
                                                  database=context.database_name)
    context.secondary_connection = psycopg2.connect(host=secondary_node_ip,
                                                    user=admin_user,
                                                    password=admin_password,
                                                    database=context.database_name)


@then(u'the postgres version is {postgres_version:d}')
def step_impl(context, postgres_version):
    min_version = postgres_version * 10000
    max_version = (postgres_version + 1) * 10000
    assert min_version <= context.primary_connection.server_version < max_version
    assert min_version <= context.secondary_connection.server_version < max_version


@then('the following extensions are installed')
def step_impl(context):
    expected_extensions = set(row['extension'] for row in context.table)
    cursor = context.primary_connection.cursor()
    cursor.execute(
        """
        SELECT extname FROM pg_extension
        """
    )
    fetched_rows = cursor.fetchall()
    actual_extensions = set(extension[0] for extension in fetched_rows)
    print('actual   extensions = ', actual_extensions)
    print('expected extensions = ', expected_extensions)
    assert expected_extensions.intersection(
        actual_extensions) == expected_extensions


@then('the following schemas exist')
def step_impl(context):
    expected_schemas = set(row['schema'] for row in context.table)
    cursor = context.primary_connection.cursor()
    cursor.execute(
        """
        SELECT schema_name FROM information_schema.schemata;
        """
    )
    fetched_rows = cursor.fetchall()
    actual_schemas = set(schema[0] for schema in fetched_rows)
    print('actual   schemas = ', actual_schemas)
    print('expected schemas = ', expected_schemas)
    assert expected_schemas.intersection(actual_schemas) == expected_schemas
