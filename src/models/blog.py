import uuid
import datetime
from src.common.database import Database
from src.models.post import Post


                                                                    #### BLOG CLASS ####

class Blog(object):
    def __init__(self,author,title,description,author_id,_id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self,title,content,date=datetime.datetime.now()):
        p = Post(blog_id=self._id, title=title, author=self.author, content=content, created_date=date)
        p.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
                "author":self.author,
                "author_id":self.author_id,
                "title":self.title,
                "description":self.description,
                "_id":self._id
                }

    @classmethod
    def get_from_mongo(cls,id):
        blog_data = Database.find_one(collection="blogs",query={'_id': id})
        return cls(**blog_data[0])
        #return cls(author=blog_data[0]['author'], title=blog_data[0]['title'], description=blog_data[0]['description'], _id=blog_data[0]['_id'])

    @classmethod
    def find_by_author_id(cls, id):
        blog_data = Database.find(collection="blogs", query={'author_id': id})
        return [cls(**blog) for blog in blog_data]
