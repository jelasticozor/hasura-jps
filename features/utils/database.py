from softozor_test_utils.timing import fail_after_timeout


def database_contains_table(database_connection, table_name, timeout_in_sec=120, period_in_sec=0.1):
    def test_table():
        cursor = database_connection.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
               SELECT FROM pg_tables
               WHERE  tablename  = %s
            );
            """, (table_name,))
        return cursor.fetchone()[0]

    return fail_after_timeout(lambda: test_table(), timeout_in_sec, period_in_sec)
