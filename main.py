import sys
import argparse
import psycopg2     # pip install -U psycopg2-binary
from config.config import host, user, password, db_name

def pasre_args(args):
    """Doc"""
    arguments = {}
    parser = argparse.ArgumentParser(description="It's a command parser for arguments")

    # adding arguments
    parser.add_argument(
        '-students',
        default='',
        action='store',
        dest='students_path',
        type=str,
        required=True,
        help='Add the path of your students file.'
    )
    parser.add_argument(
        '-rooms',
        default='',
        action='store',
        dest='rooms_path',
        type=str,
        required=True,
        help='Add the path of your rooms file.'
    )
    parser.add_argument(
        '-store_format',
        default='',
        action='store',
        dest='store_format',
        type=str,
        required=True,
        help='Choose store file format JSON or XML.'
    )

    # args
    args = parser.parse_args()
    # print('Args: ', args, type(args))

    # result
    words = ['students_path', 'rooms_path', 'store_format']
    for word in words:
        work = 'args' + '.' + word
        arguments.update({word: eval(work)})

    return arguments

def main():
    arguments = pasre_args(sys.argv[1:0])

    students_path = arguments['students_path']
    rooms_path = arguments['rooms_path']
    store_format = arguments['store_format']
    # print(students_path, rooms_path, store_format, sep='\n')

    try:
        # connect to exist db
        connecton = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connecton.autocommit = True

        with connecton.cursor() as cursor:
            cursor.execute(
                f"""COPY rooms FROM '{rooms_path}' DELIMITER ',' CSV HEADER;"""
            )

        with connecton.cursor() as cursor:
            cursor.execute(
                f"""COPY students FROM '{students_path}' DELIMITER ',' CSV HEADER;"""
            )
    except Exception as ex:
        print(ex)
    finally:
        if connecton:
            connecton.close()
            print('close connection')


# python main.py -students='/home/tonipaltus/Innowise/python_intro/data/students.csv' -rooms='/home/tonipaltus/Innowise/python_intro/data/rooms.csv' -store_format='JJJJ'
if __name__ == '__main__':
    main()