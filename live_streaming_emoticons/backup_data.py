from redis_adapter import RedisKeys


class BackupDataManager:
    def __init__(self, redis_instance, reactions_table):
        self.redis_instance = redis_instance
        self.reactions_table = reactions_table

    def __write_data_to_db(self, data_list):
        for data in data_list:
            self.reactions_table.insert_into_table(
                data['user_id'],
                data['match_id'],
                data['emoticon_type'],
                data['timestamp']
            )

    def __get_data_to_backup(self):
        keys_to_dump, data_list = [], []
        redis_dict = self.redis_instance.get_dict()
        key_prefix = RedisKeys.get_match_prefix()
        for key, value in redis_dict.items():
            if key.startswith(key_prefix):
                data_list = data_list + value
                keys_to_dump.append(key)

        return data_list, keys_to_dump

    def __delete_data_from_redis(self, keys):
        for key in keys:
            self.redis_instance.delete(key)

    def run(self):
        print('Redis to DB backup started...')
        data_list, keys_to_dump = self.__get_data_to_backup()
        self.__write_data_to_db(data_list)
        self.__delete_data_from_redis(keys_to_dump)
        # self.reactions_table.print_table()
        print('Data backup ended...')
