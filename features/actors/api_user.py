import os

from softozor_graphql_client import GraphQLClient


class ApiUser:
    def __init__(self, endpoint, path_to_graphql_folder):
        self.user_id = None
        self.jwt = None
        self.__client = GraphQLClient(endpoint)
        self.username = 'test-user@example.com'
        self.__password = 'password'
        self.__path_to_graphql_folder = path_to_graphql_folder

    # region authentication

    def sign_in(self, app_id):
        variables = {
            'username': self.username,
            'password': self.__password,
            'appId': app_id
        }
        graphql_response = self.__execute_graphql_query(
            query_name='sign_in', variables=variables)
        if 'errors' not in graphql_response.payload:
            self.jwt = graphql_response.payload['data']['sign_in']['token']
        return graphql_response

    def sign_up(self, role, app_id):
        variables = {
            'email': self.username,
            'role': role,
            'appId': app_id
        }
        graphql_response = self.__execute_graphql_query(
            query_name='sign_up', variables=variables)
        if 'errors' not in graphql_response.payload:
            self.user_id = graphql_response.payload['data']['sign_up']['userId']
        return graphql_response

    def set_password(self, change_password_id):
        variables = {
            'changePasswordId': change_password_id,
            'password': self.__password
        }
        graphql_response = self.__execute_graphql_query(
            query_name='set_password', variables=variables)
        return graphql_response

    def validate_token(self):
        graphql_response = self.__execute_graphql_query(
            query_name='validate_token')
        return graphql_response

    # endregion

    def __execute_graphql_query(self, query_name, variables=None):
        query = self.__get_query_from_file(query_name)
        graphql_response = self.__client.execute(
            query=query, variables=variables, auth_token=self.jwt, run_as_admin=False)
        return graphql_response

    def __get_query_from_file(self, query_name):
        path_to_query = os.path.join(
            self.__path_to_graphql_folder, f'{query_name}.graphql')
        with open(path_to_query, 'r') as file:
            return file.read().replace('\n', '')
