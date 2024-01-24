# Import all required libraries
import requests  # interact with API
import pandas as pd  # data manipulation
from sqlalchemy import create_engine
import configparser


# create interface for configuration
config = configparser.ConfigParser()
config.read('config.ini')


# Start PostgreSQL engine
postgres_config = config['postgres']
engine = create_engine(

    f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")

# Create API request
endpoint = 'https://demodata.grapecity.com/northwind/api/v1/Orders'
api_response = requests.get(endpoint)
json_data=api_response.json()

#load into postgres
df = pd.json_normalize(json_data)
df.to_sql('orders',engine,if_exists='replace',index=False)
engine.dispose()