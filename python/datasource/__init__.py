import psycopg2
import logging


class PostgresDatasource:

    def __init__(self, host, database, user, password):
        self.logger = logging.getLogger()

        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.logger.debug("Database connection has been open")

    def insert_group_tag(self, name, language):
        cursor = self.connection.cursor()
        try:
            cursor.execute("insert into GROUP_TAG_" + language + " (name) values (%s);", (name, ))

            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as ex:
            self.logger.exception(ex)
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()

        self.logger.debug("Database connection has been closed")
