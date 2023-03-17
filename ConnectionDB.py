import psycopg2     # pip install -U psycopg2-binary
import pandas as pd

class ConnectionDB():
    """It's a class for simple connection to database.
    There are many usefull methods to work with db."""

    def __init__(self, host: str, user: str, password: str, db_name: str, store_format: str):
        """This method initializes a connection with arguments.
         host - hostname,
         user - username,
         db_name - database name,
         password - role password,
         store_format - format to store the results of queries."""

        self.__host = host
        self.__user = user
        self.__password = password
        self.__db_name = db_name
        self.__store_format = store_format

        self.__connection = self.__get_connect()

    def __del__(self):
        """This method closes the connection to database."""
        self.__connection.close()

    @classmethod
    def get_query_from_file(self, file_path: str) -> str:
        """This method creates a query from file and returns a string."""
        file = open(f'{file_path}')
        query = file.read()
        file.close()
        return query

    def __get_connect(self) -> psycopg2.connect:
        """This method create a connection to database with necessary arguments and returns it."""
        connecton = psycopg2.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__db_name
        )
        connecton.autocommit = True

        return connecton

    def execute_query(self, query: str, show=False):
        """This method executes query and can save the result into chosen store format."""
        with self.__connection.cursor() as cursor:
            cursor.execute(f"""{query}""")

            result = ''
            try:
                result = cursor.fetchall()
            except Exception as ex:
                print(ex)

            if show:
                print(result, type(result))

            if self.__store_format.lower() == '':
                return None

            if isinstance(result, list):
                if self.__store_format.lower() == 'json':
                    self.__save_to_json(result)
                elif self.__store_format.lower() == 'csv':
                    self.__save_to_csv(result)
                else:
                    print('Incorrect save format...')


    def __save_to_json(self, query_result: list):
        """This method save query result into JSON."""
        df = pd.DataFrame(query_result)
        file = df.to_json(orient='records')
        with open('saves/query_result.json', 'w') as f:
            f.write(file)
        print('Successfully loaded')

    def __save_to_csv(self, query_result: list):
        """This method save query result into CSV."""
        df = pd.DataFrame(query_result)
        file = df.to_csv()
        with open('saves/query_result.csv', 'w') as f:
            f.write(file)
        print('Successfully loaded')