from db import DBManager


db_manager = DBManager()
db_manager.create_db('health_dev')
db_manager.create_db('accounts_dev')
db_manager.create_db('scheduler_dev')
db_manager.select_db('accounts_dev')
db_manager.create_table('users', [{
    'type': 'str',
    'name': 'name'
}, {
    'type': 'int',
    'name': 'age'
}, {
    'type': 'str',
    'name': 'email'
}])
db_manager.insert_into_db('users', 'Sajal', 31, 'sajal.4591@gmail.com')
db_manager.insert_into_db('users', 'Sarwar Kumar', 67, 'sarwar.kumar@gmail.com')
db_manager.insert_into_db('users', 'ABC', 32, 'abc@gmail.com')
db_manager.insert_into_db('users', 'ABC1', 32, 'abc1@gmail.com')
db_manager.insert_into_db('users', 'ABC2', 36, 'abc2@gmail.com')
db_manager.create_index('users', 'age')
db_manager.select_rows('users', {'age': 36})
db_manager.update_row('users', 4, {'age': 39})
db_manager.select_rows('users', {'age': 36})
db_manager.create_table('magic_links', [{
    'type': 'str',
    'name': 'short_link'
}, {
    'type': 'str',
    'name': 'complete_link'
}])
db_manager.insert_into_db('magic_links', 'https://link.to/abcd', 'https://web.orangehealth.in/order/')
db_manager.insert_into_db('magic_links', 'https://link.to/abcd1', 'https://web.orangehealth.in/order/web/')
db_manager.select_rows('users', {})
