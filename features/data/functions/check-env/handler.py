import json


def read_secret(name):
    secret_file = open('/var/openfaas/secrets/' + name)
    secret = secret_file.read().strip()
    secret_file.close()
    return secret


def handle(req):
    result = {
        'auth-secret': read_secret('auth-secret'),
        'data-protection-secret': read_secret('data-protection-secret')
    }

    return json.dumps(result)
