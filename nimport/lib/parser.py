from .tokens import Tokens
import json


class Parser(object):
    """Parser input like - container="$container" path="$path" source="$source"
     into [$container, $path, $source]"""
    @classmethod
    def parse(self, line):
        result = {}
        # splits by spaces
        options = line.split()
        for option in options:
            if option.__contains__(Tokens.ContainerToken):
                result[Tokens.Container] = self.normalize(option.replace(
                    Tokens.ContainerToken, ""))
            elif option.__contains__(Tokens.PathToken):
                result[Tokens.Path] = self.normalize(option.replace(
                    Tokens.PathToken, ""))

            elif option.__contains__(Tokens.ProviderToken):
                result[Tokens.Provider] = self.normalize(option.replace(
                    Tokens.ProviderToken, ""))

            elif option.__contains__(Tokens.ProviderOptionsToken):
                result[Tokens.ProviderOptions] = json.loads(option.replace(
                    Tokens.ProviderOptionsToken, ""))
            elif option.__contains__(Tokens.NavigateToken):
                result[Tokens.Navigate] = json.loads(option.replace(
                    Tokens.NavigateToken, ""))
        return result

    @classmethod
    def normalize(self, data):
        data = data.replace('"', '')
        data = data.replace("'", '')
        return data
