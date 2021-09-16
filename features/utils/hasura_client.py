import os
import re

import sh


class HasuraClient:
    def __init__(self, hasura_endpoint, database_name):
        self.__cli = sh.Command('hasura')
        self.__endpoint = hasura_endpoint
        self.__database_name = database_name

    def apply_migrations(self, project_folder):
        result = self.__cli('migrate', 'apply',
                            '--endpoint', self.__endpoint,
                            '--project', project_folder,
                            '--database-name', self.__database_name,
                            '--skip-update-check')
        if result.exit_code == 0:
            return self.__get_not_present_migrations_count(project_folder) == 0
        return False

    def __get_not_present_migrations_count(self, project_folder):
        migrations_folder = self.__get_migrations_folder(project_folder)
        relevant_timestamps = [item.split('_')[0]
                               for item in os.listdir(migrations_folder)]
        statuses = self.__cli('migrate', 'status',
                              '--endpoint', self.__endpoint,
                              '--project', project_folder,
                              '--database-name', self.__database_name,
                              '--skip-update-check')
        result = 0
        for timestamp in relevant_timestamps:
            status = re.findall(f'^{timestamp}.*$',
                                str(statuses), re.MULTILINE)[0]
            result += status.count('Not Present')
        return result

    def rollback_migrations(self, project_folder):
        nb_migrations = self.__get_number_of_migrations_in_folder(
            project_folder)
        result = self.__cli('migrate', 'apply',
                            '--down', nb_migrations,
                            '--endpoint', self.__endpoint,
                            '--project', project_folder,
                            '--database-name', self.__database_name,
                            '--skip-update-check')
        if result.exit_code == 0:
            return self.__get_not_present_migrations_count(project_folder) == nb_migrations
        return False

    def __get_number_of_migrations_in_folder(self, project_folder):
        migrations_folder = self.__get_migrations_folder(project_folder)
        relevant_items = os.listdir(migrations_folder)
        return int(len(relevant_items))

    def __get_migrations_folder(self, project_folder):
        return os.path.join(project_folder, 'migrations', self.__database_name)
