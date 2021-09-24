import sh as sh


class FaasClient:
    def __init__(self, gateway_url, gateway_port, root_functions_folder, faas_config_file, username, password):
        self.__cli = sh.Command('faas-cli')
        self.endpoint = f'{gateway_url}:{gateway_port}'
        self.__root_functions_folder = root_functions_folder
        self.__faas_config_file = faas_config_file
        self.__username = username
        self.__password = password

    def login(self):
        result = self.__cli('login',
                            '-g', self.endpoint,
                            '--username', self.__username,
                            '--password', self.__password)
        return result.exit_code

    def deploy(self, function_name, env={}):
        env_options = [f'-e {key}={value}' for (key, value) in env.items()]
        result = self.__cli('deploy',
                            '--image', f'softozor/{function_name}',
                            '--name', function_name,
                            '-g', self.endpoint,
                            ' '.join(env_options))
        return result.exit_code


class FaasClientFactory:
    def __init__(self, root_functions_folder, gateway_port, faas_config_file):
        self.__root_functions_folder = root_functions_folder
        self.__gateway_port = gateway_port
        self.__faas_config_file = faas_config_file

    def create(self, gateway_url, username, password):
        return FaasClient(gateway_url, self.__gateway_port, self.__root_functions_folder, self.__faas_config_file,
                          username, password)
