## How to start the application and what to expect?
- Go to your terminal and type in the command `python3 main.py`.
- There will be 3 operations that will be happening once you start the application, these are -
1. A POST method call that will run a separate thread in an infinite loop, which will keep on posting new emoticons for random matches and random users.
(You can set the max no of matches, and max no of users in config.py)
2. A GET method call in async operation every 5 seconds which will retrieve the weighted mean of the emoticon count.
3. An async call that runs every 10 seconds which takes the data backup (only the match data) from Redis and dump it into the DB layer.
(If you want to see the DB output, uncomment line no. 38 in backup_data.py)
4. How to exit the program - do a ctrl-c twice.

## Assumptions
- Redis and DB layers are created as an abstraction, it actually stores the data in memory.
- Weighted mean is taken as ceil(actual_count/1000).

## Redis Architecture
Redis is storing the data in 2 formats, one for fast retrieval of emoticon count match wise, and other for actual user data, which includes user_id, match_id, emoticon used, the timestamp when the emoticon was used by the user, etc.
A snapshot of Redis datastore is given below -

```
{
    "5_heart": 554,
    "5_sad": 198,
    "5_happy": 23,
    "6_happy": 95,
    "match_data_5": [
        {
            'user_id': 6,
            'emoticon_type': 'sad',
            'timestamp': 1670051582.545891,
            'match_id': 5
        },
        {
            'user_id': 9,
            'emoticon_type': 'happy',
            'timestamp': 1670051583.545891,
            'match_id': 5
        },
        {
            'user_id': 98,
            'emoticon_type': 'heart',
            'timestamp': 1670051584.545891,
            'match_id': 5
        },...
    ],
    "match_data_6": [
        {
            'user_id': 87,
            'emoticon_type': 'sad',
            'timestamp': 1670051581.545891,
            'match_id': 6
        },...
    ]
}
```

The key "5_heart" goes with the format of `{match_id}_{emoticon_type}` and will store the total count of an emoticon used for that combination of match and emoticon. -> Aggregated data for faster access by GET Method
The key "match_data_5" goes with the format of `match_data_{match_id}` and this stores the actual list of the emoticons used by different users at different intervals of time. -> The complete data that can be used for analysis later (by dumping it into SQL/NoSQL database)
An async operation will run every 10 seconds that takes all the keys that follows the format `match_data_{match_id}` (i.e. the complete match data) and dumps the data into the Database and once that is done, it deletes the data from Redis so that it has space for more data to come.

## DB Architecture
The DB has one model/table and here are the keys that it stores -
```
ReactionsTable
--------------
id -> the autoincrement Primary Key
user_id -> the user_id of the user who had posted the emoticon
match_id -> the match_id of the match for which the user had used the emoticon for
emoticon_type -> the actual emoticon used (can be an enum, example - sad, happy, heart)
timestamp -> the time when the user posted the emoticon
```
Assumption - Not using the other tables, but we can have `matches`, `users`, etc table as well which stores the metadata of these entities.

## Some Explanations
#### Why are we storing the data in Redis and then dumping it async into the DB?
To make faster writes with low latency, directly storing the data in DB will be costly and the number of concurrent users are too high, having low latency writes is required for such scale. Hence we are saving the data in Redis and then asynchornously (prefarrably in a different server than the application server) we are storing the data in DB and freeing up Redis thereafter.

#### How are reads happening?
We are storing the aggregate data in Redis under keys `{match_id}_{emoticon_type}` for faster retrieval. We can also take this data from DB using SQL aggregate query as given below -
```
select count(id), emoticon_type
from reactions_table
where match_id = {match_id}
group by emoticon_type
```
The above aggregation query will take time, while a simple redis get of this aggregated data will be far quicker, hence the reads happen via Redis get operation.

## Data Flow/Program Flow
#### POST Emoticon Flow
- `main.py` will run the POST method in an infinite loop that will keep posting the emoticon using the POSTMethod od `api_layer.py` in a separate thread.
- Once the flow reaches `api_layer.py -> POSTMethod`, the aggregated value (for key `{match_id}_{emoticon_type}`) of the emoticon is stored in redis using `RedisAdapter` layer.
- After this the actual data (which includes user_id, match_id, emoticon_used, current_timestamp) is stored in Redis as well under the key `match_data_{match_id}`. The dictionary is appended to the value of this key. This data will then further get stored in DB using an async operation.

#### GET Emoticon Flow
- `main.py` runs an async operation every 5 seconds which calls the `GETMethod` of the `api_layer.py`. The API layer retrieves the emoticon values of the match using the key `{match_id}_{emoticon_type}` from Redis (low latency and faster gets), perform a weighted mean and returns the data to the user. (No costly DB calls).

#### DB Backup/Data Dump
- `main.py` runs an async operation every 10 seconds which calls the `BackupDataManager` of `backup_data.py`. The purpose of this manager is to retrieve all the match data from redis which are under the key `match_data_{match_id}`.
- This includes the following Redis data -
```
    ...
    "match_data_5": [
        {
            'user_id': 6,
            'emoticon_type': 'sad',
            'timestamp': 1670051582.545891,
            'match_id': 5
        },
        {
            'user_id': 9,
            'emoticon_type': 'happy',
            'timestamp': 1670051583.545891,
            'match_id': 5
        },
        {
            'user_id': 98,
            'emoticon_type': 'heart',
            'timestamp': 1670051584.545891,
            'match_id': 5
        },...
    ],
    "match_data_6": [
        {
            'user_id': 87,
            'emoticon_type': 'sad',
            'timestamp': 1670051581.545891,
            'match_id': 6
        },...
    ]
    ...
```
- The BackupDataManager then reads these key, value pairs from Redis, inserts the data in `ReactionsTable` of the `db.py`.
- After the above step is completed, it removes/deletes these key, value pairs from Redis to free up the space.
