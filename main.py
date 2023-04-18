from flask import Flask, render_template, request, redirect, send_from_directory, abort

from flask_login import LoginManager, login_required , login_user, current_user, logout_user                  

import pymysql
import pymysql.cursors

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'something_random'

class User:
    def __init__(self, id, username, banned):
        self.is_authenticated = True
        self.is_anonymous = False
        self.is_active = not banned

        self.username = username
        self.id = id

    def get_rid(self):
        return str(self.id)



@app.route("/")
def index():
    print("despondentdemon")
    return render_template("home.html.jinja")




connection = pymysql.connect(
    host ='10.100.33.60',
    user='kwilliams3',
    password='223686940',
    database='kwilliams3_social_phones',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

@login_manager.user_loader
def user_loader(user_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * from `users` WHERE `id` = " + user_id)

    result = cursor.fetchone()

    if result is None:
        return None
    
    return User(result['id'], result['username'], result['banned'])

@app.route('/feed')
@login_required
def post_feed():

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `post` JOIN `Users` ON `Posts`.`user_id` = `Users`. `id` Order by `date` DESC;")

    results = cursor.fetchall()

    return render_template(
        "feed.html.jinja", 
        posts = results
        )

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    cursor = connection.cursor()

    photo = request.files['post_image']

    file_name = photo.filename

    file_extension = file_name.split('.')[-1]

    user_id = current_user.id

    cursor.execute("INSERT INTO")

    return redirect('/feed')


@app.route('/sign-out')
def sign_out():
    logout_user()

    return redirect('/sign-in')

@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
     if current_user.is_authenticated:
         return redirect('/feed')
     if request.method == 'POST':
        return render_template("sign_in.html.jinja")
    
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
      return redirect('/feed')
    if request.method == 'POST':
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM `users` WHERE `username` = '{request.form['username']}'")

        result = cursor.fetchone()

        if result is None:
            return render_template("sign_.html.jinja")
        
        if request.form['password'] == result['password']:
            user = User(result['id'], result['username'], result['banned'])

            login_user(user)

            return redirect('/feed')

        photo = request.files ['photo']

        file_name = photo.filename # my_photo.jpg

        file_extension = file_name.split('.')[-1]

        if file_extension in ['jpg','jpeg', 'png', 'gif']:
            photo.save('media/users/' + file_name)
        else:
            raise Exception('Invalid file type') 

        cursor.execute("""
            INSERT INTO `user` (`username`, `email`, `display_name`, `password`, `bio`, `photo`)
            VALUES(%s, %s, %s, %s, %s, %s,)
        """, (request.form['username'], request.form['email'], request.form['display_name'], request.form ['password'], request.form ['bio'], file_name))

        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")


if __name__ == '__main__':
    app.run(debug=True)

    @app.route('/Profile/<username>')
    def user_Profile(username):
        cursor = connection.cursor
        cursor.execute("SELECT * FROM `users` WHERE `username` = %s",username)

        result = cursor.fetchone()

        return render_template("user_profile.html.jinja")
    @app.get('/media/<path:path>')
    def send_media(path):
        return send_from_directory('media',path)

@app.route('/post', methods=['POST'])
@login_required
def create_post():

    user_id = current_user.id

    cursor = connection.cursor()

    Profile =request.files['File']
    
    file_name = Profile.filename # my_jgp
    
    file_extension = file_name.split('.')[-1]

    if file_extension in ['jpg','jpeg', 'png', 'gif']:
        Profile.save('media/posts/' + file_name)

    else:
        raise Exception('Invalid file type')

    cursor.execute(
        """INSERT INTO `posts` (`user_id`,`post_image`, `post_text`) VALUES (%s,%s,%s)""",
        (user_id, file_name, request.form['Post'])
    )
    
    return redirect('/feed')

@app.route('/profile/<username>')
def user_profile(username):
    cursor=connection.cursor()

    cursor.execute("SELECT * FROM `Users` WHERE `Username` = %s",(username))

    result = cursor.fetchone()

    if result is None:
        abort(404)

    cursor.close()
       
    cursor = connection.cursor()
        
    cursor.execute("SELCT * FROM `post` WHERE `user_id` = %s",(result['id']))
    
    post_result = cursor.fetchall()


    return render_template("user_profile.html.jinja",user=result)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_status.html.jinja'),404



if __name__ == '__main__':
    app.run(debug=True)
    