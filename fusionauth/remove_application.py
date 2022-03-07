import argparse

from fusionauth.fusionauth_client import FusionAuthClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', required=True, type=str, action='store')
    parser.add_argument('--api-key', required=True, type=str, action='store')
    parser.add_argument('--app-id', required=True, type=str, action='store')
    args = parser.parse_args()

    client = FusionAuthClient(args.api_key, args.api_url)
    response = client.delete_application(args.app_id)

    exit(not response.was_successful())
