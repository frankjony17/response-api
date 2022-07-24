
import os

DB_PORT = os.environ.get("DB_PORT", 5432)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "temp_test_db")
DB_USER = os.environ.get("DB_USER", "temp_test_user")
DB_PASS = os.environ.get("DB_PASS", "temp_test_pass")
DB_SCHEMA = os.environ.get("DB_SCHEMA", "controller")

TODO1 = "Serviço fornecido pelo FkSolutions."
TODO2 = "Cliente FK que consome serviços do FkSolutions."
