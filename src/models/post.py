import uuid
import datetime
from src.common.database import Database


                                                                #### POST CLASS ####


class Post(object):
    def __init__(self,blog_id,title,author,content,_id=None,created_date=datetime.datetime.now()):
        self.title = title
        self.author = author
        self.blog_id = blog_id
        self._id = uuid.uuid4().hex if _id is None else _id
        self.content = content
        self.created_date = created_date

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return {'_id':self._id,
                'blog_id':self.blog_id,
                'author':self.author,
                'title':self.title,
                'content':self.content,
                'created_date':self.created_date}

    @classmethod
    def from_mongo(cls,id):
        post_data = Database.find_one(collection='posts', query={'_id':id})
        return cls(**post_data[0])
        #return cls(blog_id=post_data[0]['blog_id'], title=post_data[0]['title'], author=post_data[0]['author'], content=post_data[0]['content'], _id=post_data[0]['_id'], created_date=post_data[0]['created_date'])

    @classmethod
    def from_blog(cls,id):
        return [cls(**post) for post in Database.find(collection='posts', query={'blog_id': id})]