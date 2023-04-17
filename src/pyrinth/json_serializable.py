class JsonSerializable:
    @classmethod
    def from_json(cls, json):
        instance = cls(**json)
        for key, value in json.items():
            setattr(instance, key, value)
        return instance

    def to_json(self) -> dict:
        return self.__dict__
