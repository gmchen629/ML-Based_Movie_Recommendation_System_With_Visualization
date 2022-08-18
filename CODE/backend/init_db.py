import sqlite3
from sqlite3 import Error
import csv

db_name = 'database'

# create table + insert data from data/*.csv files
def init_db():
    connection = connect_db()

    create_table("movie_music", connection)
    create_table("music_from_mv", connection)
    create_table("movie_from_mv", connection)

    create_table("user_feedback", connection)
    create_table("movie_feedback", connection)
    create_table("music_feedback", connection)

    insert_data("movie_music", './data/movie_music.csv', connection)
    insert_data("music_from_mv", './data/music_recommendations.csv', connection)
    insert_data("movie_from_mv", './data/movie_recommendations.csv', connection)

    #insert_feedback('user_feedback', [8,8,8,8,8,8,8,8,8], connection)
    #Insert_feedback('movie_feedback', [8,8,8,8,10,9,8,8,8], connection)
    #insert_feedback('music_feedback', [8,9,8,7,8,9,9,8,8], connection)

    #insert_new_feedback('user_feedback', [8,8,8,8,8,8,8,8,8])
    #insert_new_feedback('movie_feedback', [8,8,8,8,10,9,8,8,8])
    #insert_new_feedback('music_feedback', [8,9,8,7,8,9,9,8,8])

    return connection

# return sqlite handler for db_name
def connect_db():
    try:
        connection = sqlite3.connect(db_name)
        # connection.text_factory = str
        connection.row_factory = sqlite3.Row
        print("Connected database successfully!")
        return connection
    except Error:
        print("Error occurred: " + str(e))

# create table + insert data from data/*.csv files
def create_table(tbname, connection):
    try:
        drop_sql = "DROP TABLE IF EXISTS " + tbname
        connection.execute(drop_sql)
        if (tbname == "movie_music"):
            insert_sql = "create table movie_music (movie_id integer, movie_title text, music_name text)"
            connection.execute(insert_sql)
        elif tbname == "music_from_mv":
            insert_sql = "create table music_from_mv (movie_id integer primary key, recommendation text)"
            connection.execute(insert_sql)
        elif tbname == "movie_from_mv":
            insert_sql = "create table movie_from_mv (movie_id integer primary key, recommendation text)"
            connection.execute(insert_sql)
        elif tbname == "user_feedback":
            insert_sql = "create table user_feedback (user_feedback integer)"
            connection.execute(insert_sql)
        elif tbname == "movie_feedback":
            insert_sql = "create table movie_feedback (movie_feedback integer)"
            connection.execute(insert_sql)
        elif tbname == "music_feedback":
            insert_sql = "create table music_feedback (music_feedback integer)"
            connection.execute(insert_sql)
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Create table={} successfully!".format(tbname))

def insert_data(tbname, file_path, connection):
    # insert data
    try:
        with open(file_path, encoding = 'utf8') as f:
            file = csv.reader(f)
            for data in list(file):
                if (tbname == "movie_music"):
                    connection.execute("insert into movie_music values(?,?,?)",(data[0],data[2],data[5]))
                elif tbname == "music_from_mv":
                    connection.execute("insert into music_from_mv values(?,?)",(data[1],data[3]))
                elif tbname == "movie_from_mv":
                    connection.execute("insert into movie_from_mv values(?,?)",(data[1],data[2]))
        connection.commit()
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Insert data from {} successfully!".format(file_path))


def insert_feedback(tbname, feedback_data: list, connection):
    try:
        for feedback in feedback_data:
            if tbname == "user_feedback":
                connection.execute("insert into user_feedback values(?)",(str(feedback),))
            elif tbname == "movie_feedback":
                connection.execute("insert into movie_feedback values(?)",(str(feedback),))
            elif tbname == "music_feedback":
                connection.execute("insert into music_feedback values(?)",(str(feedback),))
            connection.commit()
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Insert data from {} file successfully!".format(tbname))


def insert_new_feedback(tbname, feedback_data: list):
    try:
        connection = sqlite3.connect('database')
        cursor = connection.cursor()
        for feedback in feedback_data:
            if tbname == "user_feedback":
                connection.execute("insert into user_feedback values(?)",(str(feedback),))
            elif tbname == "movie_feedback":
                connection.execute("insert into movie_feedback values(?)",(str(feedback),))
            elif tbname == "music_feedback":
                connection.execute("insert into music_feedback values(?)",(str(feedback),))
            connection.commit()
    except Error as e:
        print("Error occurred: " + str(e))
        return
    print("Insert new {} successfully!".format(tbname))

def query_user_feedback(connection):
    try:
        cursor = connection.cursor()
        query = "select avg(user_feedback) as avg_user_feedback from " + "user_feedback"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # print("Query executed successfully")
        return data[0]['avg_user_feedback']

    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_movie_feedback(connection):
    try:
        cursor = connection.cursor()
        query = "select avg(movie_feedback) as avg_movie_feedback from " + "movie_feedback"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # print("Query executed successfully")
        return data[0]['avg_movie_feedback']

    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_music_feedback(connection):
    try:
        cursor = connection.cursor()
        query = "select avg(music_feedback) as avg_music_feedback from " + "music_feedback"
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        # print("Query executed successfully")
        return data[0]['avg_music_feedback']
    except Error as e:
        print("Error occurred: " + str(e))
        return

# return a list of row# (in music_recommendations.csv) of the recommended tracks if tbname='music_from_mv'
# or a list of movie_id (in movie_recommendations.csv) of the recommended movies if tbname='movie_from_mv'
def query_recommendation(connection, movie_id, tbname):
    try:
        cursor = connection.cursor()
        query = "select recommendation from " + tbname + " where movie_id = " + str(movie_id)
        # print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) == 0:
            return None
        # print("Query executed successfully")
        else:
            return data[0]['recommendation']

    except Error as e:
        print("Error occurred: " + str(e))
        return

# return title of movie with id==movie_id
def query_movie_name(connection, movie_id):
    try:
        cursor = connection.cursor()
        query = "select movie_title from " + "movie_music" + " where movie_id = " + str(movie_id) + " limit 1"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) != 1:
            print(f"WARN: query_movie_name: found {len(rows)} movie_id for movie_id = \'{movie_id}\'")
            for r in rows:
                title = r['movie_title']
                print(f'\t{title}')
            return None
        return rows[0]['movie_title']
    except Error as e:
        print("Error occurred: " + str(e))
        return

def query_movie_id(connection, movie_name):
    try:
        cursor = connection.cursor()
        query = f"select distinct movie_id from movie_music where movie_title = '{movie_name}';"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) != 1:
            print(f"WARN: query_movie_id: found {len(rows)} movie_id for movie_name = \'{movie_name}\'")
            return None
        else:
            return rows[0]['movie_id']
    except Error as e:
        print("Error occurred: " + str(e))

def build_music_name_movie_id_query(recommended_music_row_no_list):
    if len(recommended_music_row_no_list) == 0:
        return None
    # query = "select * from (select row_number() over (order by (select 0)) as row_no, * from movie_music) where "
    query = "select rowid, * from movie_music where "
    for row_no in recommended_music_row_no_list:
        # query += f"row_no = {row_no+2} or "
        query += f"rowid = {row_no+2} or "
    query = query[:len(query)-4] + ";"
    return query

def query_music_name_movie_id(connection, recommended_music_row_no_list):
    query = build_music_name_movie_id_query(recommended_music_row_no_list)
    data = []
    if query is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except Error as e:
        print("Error occurred: " + str(e))
    return [{
        'row_no': d['rowid'],
        'movie_id': d['movie_id'],
        'movie_title': d['movie_title'],
        'music_name': d['music_name']
    } for d in data]

def build_movie_name_movie_id_query(recommended_movie_id_list):
    if len(recommended_movie_id_list) == 0:
        return None
    query = "select distinct movie_id, movie_title from movie_music where "
    for id in recommended_movie_id_list:
        query += f"movie_id = {id} or "
    query = query[:len(query)-4] + ";"
    return query

def query_movie_name_movie_id(connection, recommended_movie_id_list):
    query = build_movie_name_movie_id_query(recommended_movie_id_list)
    if query is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except Error as e:
        print("Error occurred: " + str(e))
    return [{
        'movie_id': d['movie_id'],
        'movie_title': d['movie_title']
    } for d in data]

def get_movie_name_id(connection, movie):
    try:
        movie_id = int(movie)
        movie_name = query_movie_name(connection, movie_id)     # FIXME: what if no such movie_id exists?
    except ValueError:
        movie_name = str(movie)
        movie_id = query_movie_id(connection, movie_name)
    finally:
        return movie_id, movie_name


# get music recommendations from a given movie
# param: a movie_id or movie_name
def get_music_recommendations(movie):
    connection = connect_db()
    movie_id, movie_name = get_movie_name_id(connection, movie)
    if movie_id is None or movie_name is None:
        print(f'WARN: get_music_recommendations: cannot no such movie = \'{movie}\' in database, no children returned')
        children = []
    else:
        recommended_music_row_no_str = query_recommendation(connection, movie_id, 'music_from_mv')
        if recommended_music_row_no_str == None:
            print(f'WARN: get_music_recommendations: cannot no such movie = \'{movie}\' in database, no children returned')
            children = []
        else:
            recommended_music_row_no_list = [int(i) for i in recommended_music_row_no_str.strip('][').split(', ')][:10]
            recommended_music_info = query_music_name_movie_id(connection, recommended_music_row_no_list)
            children = [{
                'name': music['music_name'],
                'movie_id': music['movie_id'],
                'movie_title': music['movie_title'],
                'type': 'music'
            } for music in recommended_music_info]

    connection.close()
    print("We have " + str(len(children)) + " music to recommend")
    return {
        'movie_id': movie_id,
        'movie_name': movie_name,
        'children': children
    }

# TODO: implement
def get_movie_recommendations(movie):
    connection = connect_db()
    movie_id, movie_name = get_movie_name_id(connection, movie)
    if movie_id is None or movie_name is None:
        print(f'WARN: get_movie_recommendations: cannot no such movie = \'{movie}\' in database, no children returned')
        children = []
    else:
        recommended_movie_id_str = query_recommendation(connection, movie_id, 'movie_from_mv')
        if recommended_movie_id_str == None:
            print(f'WARN: get_music_recommendations: cannot no such movie = \'{movie}\' in database, no children returned')
            children = []
        else:
            recommended_movie_id_list = [int(id) for id in recommended_movie_id_str.strip('][').split(', ')][:10]
            recommended_movie_info = query_movie_name_movie_id(connection, recommended_movie_id_list)
            children = [{
                'name': m['movie_title'],
                'movie_id': m['movie_id'],
                'type': 'movie'
            } for m in recommended_movie_info]
    
    connection.close()
    print("We have " + str(len(children)) + " movies to recommend")
    return {
        'movie_id': movie_id,
        'movie_name': movie_name,
        'children': children
    }

if __name__== '__main__':
    try:
        db = init_db()
        print("music feedback is " + str(query_music_feedback(db)))
        print("movie feedback is " + str(query_movie_feedback(db)))
        print("user feedback is " + str(query_user_feedback(db)))
        # db = init_db('database')
        # print(get_music_recommendations(db, '11860'))
    except Error as e:
        print("Error occurred: " + str(e))
