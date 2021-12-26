from python.datasource import PostgresDatasource
import logging


class CommandExecutor:

    def __init__(self, data_source):
        self.data_source = data_source
        self.logger = logging.getLogger()

    def exec_add_group(self, group_tag: str, language: str):
        self.data_source.insert_group_tag(group_tag, language)

    def exec_add_response(self, response: str, group_tag: str, language: str):
        self.data_source.insert_response(response, group_tag, language)

    def exec_add_pattern(self, pattern: str, group_tag: str, language: str):
        """group_id = self.data_source.get_group_tag_id(group_tag, language)

        if not group_id:
            return "No such group has been found \"{}\"".format(group_tag)"""

        self.data_source.insert_pattern(pattern, group_tag, language)
