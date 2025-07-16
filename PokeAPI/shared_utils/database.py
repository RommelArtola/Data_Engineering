from shared_utils.config import config_parse
from shared_utils.utils import PROJECT_DIRECTORY
import psycopg2 as pg2
import streamlit as st



config_file = PROJECT_DIRECTORY / 'shared_utils' / 'database.ini'
config_section_test = 'postgresql_test'
config_section_prod_admin = 'postgresql_prod_admin'
config_section_prod_readonly = "postgresql_prod_readonly"



class PostgreSQL:

    def __init__(self, config_file=config_file, 
                 section_name:str='user',
    ):
        self.config_file = config_file
        if section_name == 'admin':
            self.section_name = config_section_prod_admin
        else:
            self.section_name = config_section_prod_readonly


    def _connect(self):
        connection = None
        try:
            params = config_parse(self.config_file, self.section_name)
                        
            # print('Connecting to PostgreSQL Database')
            connection = pg2.connect(**params)
            return connection
        
        except (Exception, pg2.DatabaseError) as error:
            print('Connetion Failed')
            print(error)
    
    def _check_params(self, params):
        if not isinstance(params, (set, list, tuple)) and params is not None:
            raise TypeError(
                f"Params must be a set or a list, not {type(params)}"
            )
    
    def create_table(self, query_statement):
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query_statement)
            conn.commit()
            print('If it did not exists, table has been created')
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def drop_table(self, table_name):
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
            conn.commit()
            print('Table dropped if existed')
        except Exception as e:
            print(f"Error dropping table: {e}")
        finally:
            cursor.close()
            conn.close()

    def insert_record(self, insert_statement, params=None):
        self._check_params(params=params)
        
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(insert_statement, params)
                conn.commit()
                print('Values inserted')

        except Exception as e:
            print(f"Error Inserting Values: {e}")
        finally:
            conn.close()
    
    def insert_many(self, insert_statement, params_list):
        if not params_list or not isinstance(params_list, list):
            raise TypeError(
                "params_list must be a non-empty list of tuples."
            )
        
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.executemany(insert_statement, params_list)
                conn.commit()
                print(f'{len(params_list)} records inserted')

        except Exception as e:
            print(f"Error Inserting Values: {e}")
        finally:
            conn.close()



    def delete_all_records(self, table_name):
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(f'DELETE FROM {table_name};')
                conn.commit()
                print('Records cleared from table')

        except Exception as e:
            print(f"Error Inserting Values: {e}")
        finally:
            conn.close()



    def run_query(self, query_statement, params=None):
        self._check_params(params=params)

        ret = {}
        conn = self._connect()
        if conn is None or conn.closed:
            print("Connection is currently closed or failed.")
            return ret

        try:
            with conn.cursor() as cursor:
                cursor.execute(query_statement, params)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] 
                ret = {col: [] for col in columns}

                for row in rows:
                    for col, val in zip(columns, row):
                        ret[col].append(val)

                return ret
            
        except Exception as e:
            print(f"Error running query: {e}")
            return ret
        finally:
            conn.close()
