from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, name):
        if name is None or name == "":
            raise ValueError("Name must be entered")
        existing_author = Author.query.filter(
            db.func.lower(Author.name) == db.func.lower(name)
        ).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Name must be unique")
        return name


    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        phone_number_digits = "".join(filter(str.isdigit, phone_number))
        if len(phone_number_digits) != 10:
            raise ValueError("Phone number must be 10 digits")
        return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content is less than 250 characters')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary is more than 250 characters')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category should be Fiction or Non-Fiction")
        return category
    
    @validates('title')
    def validate_clickbait(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top" ,"Guess"]
        if not any(word in title for word in clickbait):
            raise ValueError("The title is not clicknbait-y enough")
        return title

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"
