from flask import Flask, render_template, request

import pymysql
import pymysql.cursors

app = Flask(__name__)

@app.route("/")
def index():
    print("despondentdemon")
    return render_template("home.html.jinja")

if __name__ == '__main__':
    app.run(debug=True)


connection = pymysql.connect(
    host ='10.100.33.60',
    user='Kwilliams3',
    password='223686940',
    database='kwilliams3_social_phones',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

app.route('/feed')
def post_feed():

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `post` ORDER BY `timestamp`")

    results = cursor.fetchall()

    return render_template(
    "feed.html.jinja",
    posts=results
)

@app.route('/sign-in')
def sign_in():
    return render_template("sign_in.html.jinja")
    
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        # Handle signup
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO `user` (`username`, `email`, `display_name`, `pasword`, `bio`, `photo`)
            VALUES(%s, %s, %s, %s, %s, %s,)
        """, ())

        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")

