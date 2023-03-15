import sys
import psycopg2     # pip install -U psycopg2-binary
from config.config import host, user, password, db_name
from functions.parse_args import pasre_args

def main():
    arguments = pasre_args(sys.argv[1:0])

    students_path = arguments['students_path']
    rooms_path = arguments['rooms_path']
    store_format = arguments['store_format']
    print(students_path, rooms_path, store_format, sep='\n')

    try:
        # connect to exist db
        connecton = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connecton.autocommit = True

        # with connecton.cursor() as cursor:
        #     cursor.execute(
        #         f"""COPY rooms FROM '{rooms_path}' DELIMITER ',' CSV HEADER;"""
        #     )
        #
        # with connecton.cursor() as cursor:
        #     cursor.execute(
        #         f"""COPY students FROM '{students_path}' DELIMITER ',' CSV HEADER;"""
        #     )
    except Exception as ex:
        print(ex)
    finally:
        if connecton:
            connecton.close()
            print('close connection')


# python main.py -students='/home/tonipaltus/Innowise/python_intro/data/students.csv' -rooms='/home/tonipaltus/Innowise/python_intro/data/rooms.csv' -store_format='JJJJ'
if __name__ == '__main__':
    main()