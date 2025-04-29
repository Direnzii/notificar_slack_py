import oracledb
import os


def conectar_db(oficial=False):
    if oficial:
        user = os.getenv('USER_ORACLE_OFICIAL')
        password = os.getenv('SENHA_ORACLE_OFICIAL')
        host = os.getenv('ORACLE_HOST')
        port = os.getenv('ORACLE_PORT')
        db_name = os.getenv('ORACLE_DB_NAME')

        connection = oracledb.connect(
            user=user,
            password=password,
            dsn=f"{host}:{port}/{db_name}"
        )
        return connection.cursor()
