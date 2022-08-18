import sqlite3

import flask
from flask import Flask, render_template
from flask_cors import CORS
from init_db import get_movie_recommendations, init_db, get_music_recommendations, insert_new_feedback
from get_feedback import *

app = Flask(__name__)
CORS(app)   # NOTE: enabling Access-Control-Allow-Origin for *, restriction recommended

def get_db_connection():
    conn = sqlite3.connect('test')
    conn.row_factory = sqlite3.Row
    return conn

# test function for http://127.0.0.1:5000/
@app.route('/')
def homepage():
    # data we used
    data = get_music_recommendations('11860')
    json_data = flask.jsonify(data)

    # display results in front end
    print("Flask run successfully!")
    return render_template('test.html', posts=data)


# function for http://127.0.0.1:5000/movie/<movie>
# for example http://127.0.0.1:5000/movie/888
@app.route('/movie/<movie>')
def movie_recommend_result(movie):
    data = get_movie_recommendations(movie)
    json_data = flask.jsonify(data)
    return json_data

# function for http://127.0.0.1:5000/music/<movie>
# for example http://127.0.0.1:5000/music/888
@app.route('/music/<movie>')
def music_recommend_result(movie):
    data = get_music_recommendations(movie)
    json_data = flask.jsonify(data)
    return json_data


############ the below functions are only for test ###############
@app.route('/feedback/user_feedback/<rating>')
def user_feedback(rating):
    # TODO: new feedback data should be put as the second parameters in insert_new_feedback()
    insert_new_feedback('user_feedback',[rating])

    # get current average feedback
    system_user_feedback = query_user_feedback()
    json_data = flask.jsonify(system_user_feedback)
    print("get user feedback")
    print(system_user_feedback)
    return json_data

@app.route('/feedback/movie_feedback/<rating>')
def movie_feedback(rating):
    # TODO: new feedback data should be put as the second parameters in insert_new_feedback()
    insert_new_feedback('movie_feedback',[rating])

    # get current average feedback
    movie_user_feedback = query_movie_feedback()
    json_data = flask.jsonify(movie_user_feedback)
    print("get movie feedback")
    print(movie_user_feedback)
    return json_data

@app.route('/feedback/music_feedback/<rating>')
def music_feedback(rating):
    # TODO: new feedback data should be put as the second parameters in insert_new_feedback()
    insert_new_feedback('music_feedback',[rating])

    # get current average feedback
    mousic_user_feedback = query_music_feedback()
    json_data = flask.jsonify(mousic_user_feedback)
    print("get movie feedback")
    print(mousic_user_feedback)
    return json_data

# test function for http://127.0.0.1:5000/create/
@app.route('/create/', methods=('GET', 'POST'))
def make_query():
    print("Flask run successfully!")
    return render_template('create.html')




if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3000, debug=True)
    init_db()
    app.run(port='5000', debug=True)
