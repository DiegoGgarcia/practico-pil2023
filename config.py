import os
from dotenv import load_dotenv
load_dotenv()

# Configuraciones de la base de datos
db_connector = os.getenv("DB_CONNECTOR")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_ip_address = os.getenv("DB_IP_ADDRESS")
db_name = os.getenv("DB_NAME")

# Varios
registros_por_pagina = 10
