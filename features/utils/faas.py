import requests
from softozor_test_utils import wait_until


def can_invoke_function(url, timeout_in_sec=120, period_in_sec=5):
    def invoke():
        response = requests.post(url)
        return response.status_code < 500

    try:
        wait_until(lambda: invoke(),
                   timeout_in_sec=timeout_in_sec, period_in_sec=period_in_sec)
        return True
    except TimeoutError:
        return False


def deploy(faas_client, path_to_serverless_config, function_name, env={}):
    exit_code = faas_client.deploy(
        path_to_serverless_config, function_name, env)

    if exit_code == 0:
        function_url = f'http://{faas_client.endpoint}/function/{function_name}'
        return can_invoke_function(function_url)
    else:
        return False
