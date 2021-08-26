import sh as sh


class FaasClient:
    def __init__(self, gateway_url, gateway_port):
        self.__cli = sh.Command('faas-cli')
        self.__endpoint = f'{gateway_url}:{gateway_port}'

    def login(self, username, password):
        result = self.__cli('login', '-g', self.__endpoint,
                            '--username', username, '--password', password)
        return result.exit_code
