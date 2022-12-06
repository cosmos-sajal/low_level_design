class RedisKeys:
    @staticmethod
    def get_match_prefix():
        return 'match_data_'

    @staticmethod
    def get_match_key(match_id):
        return f'{RedisKeys.get_match_prefix()}{str(match_id)}'

    @staticmethod
    def get_emoticon_key(match_id, emoticon_type):
        return f'{str(match_id)}_{emoticon_type}'


class Redis:
    def __init__(self):
        # taking a dictionary as an abstraction layer
        # over redis
        self.key_value_dict = {}

    def get(self, key):
        if key in self.key_value_dict:
            return self.key_value_dict[key]
        else:
            return None

    def set(self, key, value):
        self.key_value_dict[key] = value

    def delete(self, key):
        del self.key_value_dict[key]

    def get_dict(self):
        return self.key_value_dict


# creating only one instance of Redis,
# singleton deign pattern
class RedisAdapter:
    def __init__(self):
        self.redis = Redis()

    def get_instance(self):
        if self.redis is None:
            self.redis = Redis()

        return self.redis
