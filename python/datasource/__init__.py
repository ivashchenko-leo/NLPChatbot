import psycopg2
import logging
import python.validation as validation


class PostgresDatasource:

    def __init__(self, host, database, user, password):
        self.logger = logging.getLogger()

        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.logger.debug("Database connection has been open")

    def get_group_tag_id(self, name, language):
        cursor = self.connection.cursor()
        try:
            cursor.execute("select ID from GROUP_TAG_" + language + " where name = %s", (name, ))

            records = cursor.fetchall()

            if records:
                return int(records[0][0])
            else:
                return None
        except (Exception, psycopg2.DatabaseError) as ex:
            self.logger.exception(ex)
            self.connection.rollback()
        finally:
            cursor.close()

    def __insert(self, sql, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)

            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as ex:
            self.logger.exception(ex)
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_pattern(self, pattern, group_tag, language):
        validation.guard_alphanumeric(language, "Language must be alphanumeric string")

        sql = "insert into PATTERN_{} (TEXT, GROUP_TAG_ID) " \
              "select %s, ID from GROUP_TAG_{} where name = %s;".format(language, language)
        params = (pattern, group_tag)

        self.__insert(sql, params)

    def insert_response(self, response, group_tag, language):
        validation.guard_alphanumeric(language, "Language must be alphanumeric string")

        sql = "insert into RESPONSE_{} (TEXT, TYPE, GROUP_TAG_ID) " \
              "select %s, 'TEXT', ID from GROUP_TAG_{} where name = %s;".format(language, language)
        params = (response, group_tag)

        self.__insert(sql, params)

    def insert_group_tag(self, name, language):
        validation.guard_alphanumeric(language, "Language must be alphanumeric string")

        sql = "insert into GROUP_TAG_{} (NAME) values (%s) on conflict (NAME) do nothing;".format(language)
        params = (name,)

        self.__insert(sql, params)

    def close(self):
        if self.connection:
            self.connection.close()

        self.logger.debug("Database connection has been closed")
