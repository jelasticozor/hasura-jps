import psycopg2
import psycopg2.errors

# TODO: we should have a fixture closing all connections after each scenario


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
    context.connections = {
        'primary': psycopg2.connect(
            host=primary_node_ip,
            user=admin_user,
            password=admin_password,
            database=context.database_name),
        'secondary': psycopg2.connect(
            host=secondary_node_ip,
            user=admin_user,
            password=admin_password,
            database=context.database_name)
    }


@when(u'a user creates a dummy table on the {database} database')
def step_impl(context, database):
    database_connection = context.connections[database]
    cursor = database_connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE dummy(
                id int PRIMARY KEY NOT NULL
            );
            """
        )
        database_connection.commit()
    except psycopg2.errors.lookup('25006') as e:
        print('exception = ', e)
        context.database_error = e.diag.message_detail


@then(u'the postgres version is {postgres_version:d}')
def step_impl(context, postgres_version):
    min_version = postgres_version * 10000
    max_version = (postgres_version + 1) * 10000
    assert min_version <= context.connections['primary'].server_version < max_version
    assert min_version <= context.connections['secondary'].server_version < max_version


@then('the following extensions are installed')
def step_impl(context):
    expected_extensions = set(row['extension'] for row in context.table)
    cursor = context.connections['primary'].cursor()
    cursor.execute(
        """
        SELECT extname FROM pg_extension;
        """
    )
    fetched_rows = cursor.fetchall()
    actual_extensions = set(extension[0] for extension in fetched_rows)
    assert expected_extensions.intersection(
        actual_extensions) == expected_extensions


@then('the following schemas exist')
def step_impl(context):
    expected_schemas = set(row['schema'] for row in context.table)
    cursor = context.connections['primary'].cursor()
    cursor.execute(
        """
        SELECT schema_name FROM information_schema.schemata;
        """
    )
    fetched_rows = cursor.fetchall()
    actual_schemas = set(schema[0] for schema in fetched_rows)
    assert expected_schemas.intersection(actual_schemas) == expected_schemas


@then('she gets the error')
def step_impl(context):
    expected_error = context.text
    assert expected_error in context.database_error


@then('she sees the dummy table in the {database} database')
def step_impl(context, database):
    database_connection = context.connections[database]
    cursor = database_connection.cursor()
    cursor.execute(
        """
        SELECT EXISTS (
           SELECT FROM pg_tables
           WHERE  tablename  = %s
        );
        """, ('dummy',))
    assert cursor.fetchone()[0] is True
