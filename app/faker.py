from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from sqlalchemy.sql.expression import except_
from . import db
from .model import User,Post

def users(count=100):
    fake=Faker()
    i=0
    while i < count:
        u=User(email=fake.email(),
                username=fake.user_name(),
                password='password',
                confirmed=True,
                location=fake.city(),
                about_me=fake.text(),
                member_since=fake.past_date()
        )

        db.session.add(u)
        try:
            db.session.commit()
            i+=1
        except IntegrityError:
            db.session.rollback()
            raise

def posts(count=100):
    fake=Faker()
    user_count=User.query.count()
    for i in range(count):
        u= User.query.offset(randint(0,user_count-1)).first()
        p=Post(body=fake.text(),
        timestamp=fake.past_date(),
        author=u)
        db.session.add(u)
    db.session.commit()