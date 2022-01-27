import logging
import json
import random


class JsonDatasource:

    def __init__(self, path):
        self.logger = logging.getLogger()

        with open(path, 'r') as f:
            self.intents = json.load(f)

    def get_response(self, group_tag, language):
        responses = next(filter(lambda intent: intent['tag'] == group_tag, self.intents[language.lower()]['intents']))['responses']

        return random.choice(responses)

    def get_patterns(self, language):
        return [(intent['patterns'], intent['tag']) for intent in self.intents[language.lower()]['intents']]

    def get_response_not_found(self, language):
        return self.intents[language.lower()]['general']['responseNotFound']

    def get_certainty_threshold(self, language):
        return self.intents[language.lower()]['general']['certaintyThreshold']

    def insert_pattern(self, pattern, group_tag, language):
        pass

    def insert_response(self, response, group_tag, language):
        pass

    def insert_group_tag(self, name, language):
        pass

    def close(self):
        pass
