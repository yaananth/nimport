import abc


class Provider(abc.ABC):
    @abc.abstractmethod
    def getFile(self, container: str, path: str, options: dict):
        pass
