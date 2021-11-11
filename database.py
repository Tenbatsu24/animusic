import psycopg2
from db_config import config


class Connection:

    def __init__(self):
        self.conn = None
        self.cur = None

        try:
            params = config()
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()
            cur.execute('SET search_path = animusic, public;')

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()

            # set the connection to the acquired conn
            self.conn = conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit(0)

    def acquire(self, schema):
        if self.cur is None:
            self.cur = self.conn.cursor()
            self.cur.execute(f'SET search_path = {schema}, public;')

    def execute(self, sql):
        self.cur.execute(sql)

    def commit(self):
        if self.cur is not None:
            self.cur.close()
            self.conn.commit()

            self.cur = None

    def fetch(self):
        to_return = []

        if self.cur is not None:
            to_return = self.cur.fetchall()

        return to_return

    def close(self):
        self.conn.close()
