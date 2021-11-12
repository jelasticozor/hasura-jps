import requests
from softozor_test_utils.timing import fail_after_timeout


def faas_is_up(faas_client, timeout_in_sec=300, period_in_sec=15):
    def test_is_up():
        try:
            exit_code = faas_client.login()
            return exit_code == 0
        except:
            return False

    return fail_after_timeout(lambda: test_is_up(), timeout_in_sec, period_in_sec)


def can_invoke_function(url, timeout_in_sec=120, period_in_sec=5):
    def invoke():
        response = requests.post(url)
        return response.status_code < 500

    return fail_after_timeout(lambda: invoke(), timeout_in_sec, period_in_sec)


def is_function_ready(faas_client, function_name):
    def is_ready():
        return faas_client.is_ready(function_name)

    return fail_after_timeout(lambda: is_ready())


def deploy(faas_client, path_to_serverless_config, function_name, env={}):
    exit_code = faas_client.deploy(
        path_to_serverless_config, function_name, env)

    if exit_code == 0:
        function_url = f'http://{faas_client.endpoint}/function/{function_name}'
        return can_invoke_function(function_url)
    else:
        return False
