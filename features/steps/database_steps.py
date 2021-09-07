import psycopg2


@given(u'the database is installed')
def step_impl(context):
    print('current env name = ', context.current_env_name)
    context.jps_client.install_from_file(
        context.database_manifest, context.current_env_name)
    env_info = context.control_client.get_env_info(context.current_env_name)
    primary_node_ip = env_info.get_node_ip_from_name('Primary')
    assert primary_node_ip is not None
    secondary_node_ip = env_info.get_node_ip_from_name('Secondary')
    assert secondary_node_ip is not None
    assert 'Password' in context.manifest_data
    postgres_admin_password = context.manifest_data['Password']
    context.primary_connection = psycopg2.connect(host=primary_node_ip,
                                                  user=context.postgres_admin_username,
                                                  password=postgres_admin_password,
                                                  database=context.postgres_default_database)
    context.secondary_connection = psycopg2.connect(host=secondary_node_ip,
                                                    user=context.postgres_admin_username,
                                                    password=postgres_admin_password,
                                                    database=context.postgres_default_database)


@then(u'the postgres version is {postgres_version:d}')
def step_impl(context, postgres_version):
    min_version = postgres_version * 10000
    max_version = (postgres_version + 1) * 10000
    assert min_version <= context.primary_connection.server_version < max_version
    assert min_version <= context.secondary_connection.server_version < max_version


@then('the following extensions are installed')
def step_impl(context):
    expected_extensions = set(map(lambda row: row[0], context.table))
    cursor = context.primary_connection.cursor()
    cursor.execute(
        """
        SELECT * FROM pg_extension
        """
    )
    rows = cursor.fetchall()
    actual_extensions = set(map(lambda row: row[1], rows))
    print('actual   extensions = ', actual_extensions)
    print('expected extensions = ', expected_extensions)
    assert expected_extensions.intersection(
        actual_extensions) == expected_extensions


@then('the following schemas exist')
def step_impl(context):
    for row in context.table:
        cursor = context.primary_connection.cursor()
        cursor.execute(
            """
            SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s;
            """,
            (row['schema']))
        schema_name = cursor.fetchone()
        print('expected schema = ', row['schema'])
        print('fetched schema  = ', schema_name)
        assert schema_name is not None
