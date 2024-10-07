from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        authors = [author.name for author in Author.query.all()]
        if not name or name in authors:
            raise ValueError('Author must have a name')
        return name
        
    @validates("phone_number")
    def validate_phone_number(self, key, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must be 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Title entered is an invalid option")
        return content

    @validates("summary")
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Title entered is an invalid option")
        return value

    @validates("category")
    def validate_category(self, key, value):
        category = ['Fiction', 'Non-Fiction']
        if value not in category:
            raise ValueError('Category entered is an invalid choice')
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(title in value for title in titles):
            raise ValueError('Title must contain one of the keywords: "Won\'t Believe", "Secret", "Top", "Guess"')
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
