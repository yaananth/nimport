from nimport.lib.tokens import Tokens


class Parser(object):
    """Parser input like - container="$container" path="$path" source="$source"
     into [$container, $path, $source]"""
    @classmethod
    def parse(self, line: str):
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
        return result

    @classmethod
    def normalize(self, data: str):
        data = data.replace('"', '')
        data = data.replace("'", '')
        return data