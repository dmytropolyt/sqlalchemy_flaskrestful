#config for postgesql database
config = {'user': 'your_username',
          'password': 'your_password',
          'host': '127.0.0.1',
          'port': '5432',
          'db': 'university'}

database_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}"
test_database_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/test_database"