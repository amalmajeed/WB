from src.common.database import Database
from src.models.blog import Blog
import uuid
from flask import session


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def register(cls, email, password):
        usr = cls.get_by_email(email)
        if usr is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
        else:
            print("User already Exists ! ")
            session['email'] = None

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None


    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection="users",query={'email':email})
        print("No problem upto get by email")
        try:
            a = data[0]
            print(data[0])
            return cls(**data[0])
            #return cls(email=data[0]['email'],password=data[0]['password'],_id=data[0]['_id'])
        except IndexError:
            return None

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection="users", query={'_id': _id})
        try:
            a = data[0]
            return cls(**data[0])
        except IndexError:
            return None

    @staticmethod
    def check_login_valid(email, password):
        #Check user email and passwords match
        print("No problem upto check login valid")
        usr = User.get_by_email(email)
        if usr is None:
            print("User Doesnt exist !")
            return [False,0]
        else:
            x = usr.password == password
            if x is True:
                return [True,0]
            else:
                print("Incorrect Password !")
                return [False,1]

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {"email": self.email,
                "_id": self._id,
                "password": self.password}

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())

    def new_blog(self, title, description):
        blog = Blog(author=self.email, title= title, description= description, author_id= self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content):
        #title,author,content
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title=title,content=content)