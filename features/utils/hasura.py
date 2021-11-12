import requests
from softozor_test_utils.timing import fail_after_timeout


def hasura_is_up(hasura_ip, hasura_port, timeout_in_sec=300, period_in_sec=15):
    def test_is_up():
        try:
            response = requests.get(
                f'http://{hasura_ip}:{hasura_port}/healthz')
            return response.status_code == 200
        except:
            return False

    return fail_after_timeout(lambda: test_is_up(), timeout_in_sec, period_in_sec)
