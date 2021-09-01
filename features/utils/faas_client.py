import os

import sh as sh


class FaasClient:
    def __init__(self, gateway_url, gateway_port, root_functions_folder, faas_config_file):
        self.__cli = sh.Command('faas-cli')
        self.endpoint = f'{gateway_url}:{gateway_port}'
        self.__root_functions_folder = root_functions_folder
        self.__faas_config_file = faas_config_file

    def login(self, username, password):
        result = self.__cli('login', '-g', self.endpoint,
                            '--username', username, '--password', password)
        return result.exit_code

    # TODO: use a decorator to changedir and come back to original location
    def up(self, function_name):
        cwd = os.getcwd()
        os.chdir(self.__root_functions_folder)
        result = self.__cli('up', '-f', self.__faas_config_file,
                            '--filter', function_name, '-g', self.endpoint)
        os.chdir(cwd)
        return result.exit_code


class FaasClientFactory:
    def __init__(self, root_functions_folder, gateway_port, faas_config_file):
        self.__root_functions_folder = root_functions_folder
        self.__gateway_port = gateway_port
        self.__faas_config_file = faas_config_file

    def create(self, gateway_url):
        return FaasClient(gateway_url, self.__gateway_port, self.__root_functions_folder, self.__faas_config_file)
