import psycopg2
from profsDB import profsDB
from prof import Professor
from sys import argv, stderr

class profPreferencesDB:
    
    def __init__(self):
        self.conn = None

    def connect(self):
        error_statement = ''

        try:
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

    def createProfPreference(self, data):
        error_statement = ''

        try:
            cur = self.conn.cursor()

            # Check if user has already submitted their preferences

            # cur.execute("SELECT * FROM profs WHERE netid=%s", [prof.getNetId()])
            # result = cur.fetchone()
            # if result == None:
            # return error_statement, returned

            stmt = """INSERT INTO preferences(username, courseselection, advisor1, topiccomments1, advisor2, topiccomments2, advisor3, topiccomments3, advisor4, topiccomments4, submittedtime, completedtime) VALUES"""
            stmt += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cur.execute(stmt, data)
            self.conn.commit()
            cur.close()
        except Exception as error:
            error_statement = str(error)
            print(error_statement)

