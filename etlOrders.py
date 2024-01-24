# Import necessary libraries
import requests  # to connect to API
import pandas as pd  # for data transformation
import configparser  # to create my configurations
from sqlalchemy import create_engine  # this helps me communicate with PostgreSQL

# Create configuration interface
config = configparser.ConfigParser()
config.read('config.ini')

# Start PostgreSQL engine
postgres_config = config['postgres']
engine = create_engine(
    f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}/{postgres_config['database']}")

# Create API requests
endpoint = 'https://demodata.grapecity.com/northwind/api/v1/Orders'
api_response = requests.get(endpoint)
json_data = api_response.json()

# Print the JSON response
print(json_data)

# load data into progres
df = pd.json_normalize(json_data)
df.to_sql('orders', engine, if_exists= 'replace', index=False)
engine.dispose()