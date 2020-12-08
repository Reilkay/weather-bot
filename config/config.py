import toml


class Config:
    def __init__(self, path):
        self.path = path

    def get(self) -> dict:
        config = toml.load(self.path)
        return config


config = Config('./config.toml').get()
print(config)