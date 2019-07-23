class Tokens(object):
    Container = "container"
    Path = "path"
    Provider = "provider"
    ProviderOptions = "providerOptions"

    Equals = "="

    ContainerToken = Container + Equals
    PathToken = Path + Equals
    ProviderToken = Provider + Equals
    ProviderOptionsToken = ProviderOptions + Equals
