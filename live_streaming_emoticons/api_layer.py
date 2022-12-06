import math
import time

from config import EMOTICON_TYPES
from redis_adapter import RedisKeys


class PostMethod:
    def __init__(self, redis_instance):
        self.redis_instance = redis_instance

    def post(self, user_id, match_id, emoticon_type):
        # add the information in redis
        key = RedisKeys.get_emoticon_key(match_id, emoticon_type)

        # get the value of the previous emoticon
        value = self.redis_instance.get(key)
        if value is None:
            self.redis_instance.set(key, 1)
        else:
            self.redis_instance.set(key, value + 1)

        # stores the data of the ongoing match in redis,
        # which will be later dumped to the Database
        # key of this data will be the match_id
        match_data_key = RedisKeys.get_match_key(match_id)
        user_data = {
            'user_id': user_id,
            'emoticon_type': emoticon_type,
            'timestamp': time.time(),
            'match_id': match_id
        }
        match_data_value = self.redis_instance.get(match_data_key)
        if match_data_value is None:
            self.redis_instance.set(match_data_key, [user_data])
        else:
            match_data_value.append(user_data)
            self.redis_instance.set(match_data_key, match_data_value)

        return user_data


class GetMethod:
    def __init__(self, redis_instance):
        self.redis_instance = redis_instance

    def get(self, match_id):
        resultant_data = []

        for emoticon_type in EMOTICON_TYPES:
            key = RedisKeys.get_emoticon_key(match_id, emoticon_type)
            value = self.redis_instance.get(key)
            # assuming that weighted mean is just dividing the numbers by 1000
            # and taking the ceiling
            if value is not None:
                weighted_mean_value = math.ceil(value / 1000.0)
            else:
                weighted_mean_value = 0
            resultant_data.append({
                emoticon_type: weighted_mean_value
            })

        return resultant_data
