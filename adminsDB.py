from os import environ
from sys import argv, stderr
import psycopg2

class adminsDB:

    def __init__(self):
        self.conn = None

    def connect(self):
        error_statement = ''

        try:
            # hostname = environ.get('DATABASE_HOST')
            # username = environ.get('DATABASE_USERNAME')
            # password = environ.get('DATABASE_PASSWORD')
            # database = environ.get('DATABASE_NAME')

            hostname = 'ec2-52-200-119-0.compute-1.amazonaws.com'
            username = 'hmqcdnegecbdgo'
            password = 'c51235a04a7593a9ec0c13821f495f259a68d2e1ab66a93df947ab2f31970009'
            database = 'd99tniu8rpcj0o'

            self.conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        except Exception as e:
            error_statement = str(e)
            print(error_statement, file=stderr)

        return error_statement

    def disconnect(self):
        self.conn.close()