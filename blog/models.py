import uuid
from app import db
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from user.models import UserModel
# from slugify import slugify




class Article(db.Model):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    article_id = Column(String(200), default=uuid.uuid4())
    title = Column(String(100), nullable=False, unique=True)
    # slug = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    image = Column(String(100), default='')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'{self.title}[:-20]'
    
    # @staticmethod
    # def generate_slug(cls, value, oldvalue, initiator):
    #     if value and (not cls.slug and value != oldvalue):
    #         cls.slug = slugify(value, allow_unicode=True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def get_writer(self, user_id):
        return UserModel.query.get_or_404(user_id)
    







# db.event.listen(Article.title, 'set', Article.generate_slug, retval=False)