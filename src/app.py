from flask import Flask,render_template,request,session,make_response
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post

app = Flask(__name__) # __main__
app.secret_key = "amal"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home_page():
    if session['email'] is None:
        return render_template('login.html', message="")
    else:
        return render_template("profile.html", email=session['email'], message="", parameter=True)


@app.route('/register')
def register():
    if session['email'] == None:
        return render_template('register.html',message="")
    else:
        return render_template('profile.html',email=session['email'],message="Logout First before trying to register",parameter= True)

@app.route('/login')
def login():
    if session['email'] == None:
        return render_template('login.html',message="")
    else:
        return render_template('profile.html', email=session['email'], message="Already Logged In",parameter= True)

@app.route('/logout')
def logout():
    if session['email'] == None:
        return render_template('login.html',message="No User Logged in ! Try logging in")
    else:
        session['email'] = None
        return render_template('login.html', message="Succesfully Logged Out")


@app.route('/auth/login', methods = ['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    x = User.check_login_valid(email ,password)
    if x[0] == True:
        User.login(email)
        return render_template("profile.html", email=session['email'],message="",parameter=True)
    else:
        if x[1]==0:
            return render_template('register.html', message="User Doesnt Exist, try registering")
        else:
            return render_template('login.html',message = "Wrong password , try again")


@app.route('/auth/register', methods = ['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email, password)
    if session['email'] is None:
        return render_template("login.html" , message = "Registration failed as user already exists ! try logging in .")
    else:
        return render_template("profile.html", email=session['email'],parameter=True)

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    parameter = False
    if session['email'] is not None:
        parameter = True
    if user_id is not None:
        usr = User.get_by_id(user_id)
    else:
        usr = User.get_by_email(session['email'])

    blogs = usr.get_blogs()
    return render_template("user_blogs.html", blogs= blogs,email= usr.email,parameter=parameter)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.get_from_mongo(blog_id)
    posts = blog.get_posts()
    parameter = False
    if session['email'] is not None:
        parameter = True
    return render_template("posts.html", posts = posts,blog_title = blog.title,author = blog.author,blog_id= blog._id, parameter = parameter)


@app.route('/blogs/new' , methods = ['POST','GET'])
def create_new_blog():
    if request.method == 'GET':
        if session['email'] is None:
            return render_template("login.html",message="Login or Register to create a blog! .")
        else:
            return render_template('new_blog.html',parameter=True)
    else:
        title = request.form['title']
        description = request.form['description']
        usr = User.get_by_email(session['email'])
        new_blog = Blog(usr.email,title,description,usr._id)
        new_blog.save_to_mongo()
        return make_response(user_blogs(usr._id))

@app.route('/posts/new/<string:blog_id>' , methods = ['POST','GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html',blog_id= blog_id,parameter= True)
    else:
        title = request.form['title']
        content = request.form['content']
        #usr = User.get_by_email(session['email'])
        #blog_id,title,author,content
        new_post = Post(blog_id,title,session['email'],content)
        new_post.save_to_mongo()
        return make_response(blog_posts(blog_id))


if __name__=="__main__":
    app.run()