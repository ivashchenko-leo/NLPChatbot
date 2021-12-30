import psycopg2
import logging
import python.validation as validation


class PostgresDatasource:

    def __init__(self, host, database, user, password):
        self.logger = logging.getLogger()

        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.logger.debug("Database connection has been open")

    def __select_single(self, sql, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)

            return cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as ex:
            self.logger.exception(ex)
            self.connection.rollback()
        finally:
            cursor.close()

    def __select_multiple(self, sql, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)

            return cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as ex:
            self.logger.exception(ex)
            self.connection.rollback()
        finally:
            cursor.close()

    def get_response(self, group_tag, language):
        validation.guard_alphanumeric(language, "Language must not be null")

        sql = "select R.TEXT from RESPONSE_{} R inner join GROUP_TAG_{} GT on GT.ID = R.GROUP_TAG_ID where GT.NAME = %s" \
              " order by random() limit 1".format(language, language)
        params = (group_tag, )

        return self.__select_single(sql, params)

    def get_patterns(self, language):
        validation.guard_alphanumeric(language, "Language must be an alphanumeric string")

        sql = "select array_agg(TEXT) PATTERN, NAME from PATTERN_{} PT " \
              "inner join GROUP_TAG_{} GT on GT.ID = PT.GROUP_TAG_ID group by NAME;".format(language, language)

        return self.__select_multiple(sql, None)

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
        validation.guard_alphanumeric(language, "Language must be an alphanumeric string")

        sql = "insert into PATTERN_{} (TEXT, GROUP_TAG_ID) " \
              "select %s, ID from GROUP_TAG_{} where name = %s;".format(language, language)
        params = (pattern, group_tag)

        self.__insert(sql, params)

    def insert_response(self, response, group_tag, language):
        validation.guard_alphanumeric(language, "Language must be an alphanumeric string")

        sql = "insert into RESPONSE_{} (TEXT, TYPE, GROUP_TAG_ID) " \
              "select %s, 'TEXT', ID from GROUP_TAG_{} where name = %s;".format(language, language)
        params = (response, group_tag)

        self.__insert(sql, params)

    def insert_group_tag(self, name, language):
        validation.guard_alphanumeric(language, "Language must be an alphanumeric string")

        sql = "insert into GROUP_TAG_{} (NAME) values (%s) on conflict (NAME) do nothing;".format(language)
        params = (name,)

        self.__insert(sql, params)

    def close(self):
        if self.connection:
            self.connection.close()

        self.logger.debug("Database connection has been closed")
