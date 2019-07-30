from nimport.providers.constants import Constants


class Provider(object):
    def getFile(self, container, path, options):
        pass

    def clone(self, container, path, options):
        pass

    def get(self, container, path, options):
        if Constants.OptionsClone in options:
            return self.clone(container, path, options)
        else:
            return self.getFile(container, path, options)

    def getContainerName(self, container):
        return container
