import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name='products.db', table_name='product_data'):
        self.db_name = db_name # Veri tabanı adı
        self.table_name = table_name # Tablo adı

    #Veri tabanı giriş bağlantısını oluşturuyoruz.
    def create_connection(self):
        connection = sqlite3.connect(self.db_name)
        return connection

    # Eğer içeride bir veri tabanı yoksa veri tabanını tablolarıyla beraber oluşturuyoruzzç
    def create_table(self):
        connection = self.create_connection()
        cursor = connection.cursor()

        # İçeride veri tabanı var mı yok mu onu kontrol ediyoruz eğer varsa tekrar veri tabanı oluşturmuyor
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        if not cursor.fetchone():
            # Veritabanı yoksa oluşturuyoruz
            cursor.execute(f'''
                   CREATE TABLE {self.table_name} (
                       ID INTEGER,
                       brandName TEXT,
                       productName TEXT,
                       commentCount INTEGER,
                       price INTEGER
                   )
               ''')
        connection.commit()
        connection.close()

    # Verileri tablolara kaydediyoruz
    def write_to_database(self, data_frame):
        connection = self.create_connection()
        data_frame.to_sql(self.table_name, connection, index=False, if_exists='append')
        connection.close()

    # Veritabanından istediğimiz parametrede verileri okuyoruz
    def get_from_db_by_query(self,param):
        connection = self.create_connection()
        query = f'{param}'
        result = pd.read_sql_query(query, connection)
        connection.close()
        return result
