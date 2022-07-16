DEV_DB = 'sqlite:///orderscatalog'

pg_user = 'admin'
pg_pass = 'admin'
pg_db = 'orderscatalog'
pg_host = 'localhost'
pg_port = '5432'

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'