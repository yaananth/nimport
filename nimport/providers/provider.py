from nimport.providers.constants import Constants


class Provider(object):
    def getFile(self, container: str, path: str, options: dict):
        pass

    def clone(self, container: str, path: str, options: dict):
        pass

    def get(self, container: str, path: str, options: dict):
        if Constants.OptionsClone in options:
            return self.clone(container, path, options)
        else:
            return self.getFile(container, path, options)

    def getContainerName(self, container: str):
        return container
