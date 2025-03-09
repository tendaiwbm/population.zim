import psycopg2
from dotenv import load_dotenv,find_dotenv
import os,sys
load_dotenv(find_dotenv())



class QExecutor:
    def exec(query):
        connection = psycopg2.connect(user=os.getenv('PG_USER'),
                                      password=os.getenv('PG_PASSWORD'),
                                      host=os.getenv('HOST'),
                                      port=os.getenv('PORT'),
                                      database=os.getenv('DATABASE'),
                                      options=os.getenv('OPTIONS'))
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                connection.commit()
                return True
            except psycopg2.Error as e:
                connection.rollback()
                raise e
                return False             
