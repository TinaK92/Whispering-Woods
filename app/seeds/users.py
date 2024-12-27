from datetime import datetime
from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text

def seed_users():
    now = datetime.utcnow()

    demo = User.query.filter_by(username='Demo').first()
    if not demo:
        demo = User(
            username='Demo',
            email='demo@aa.io',
            password='password',
            first_name='Demo',
            last_name='User',
            role='admin',
            created_at=now,
            updated_at=now
        )
    marnie = User.query.filter_by(username='marnie').first()
    if not marnie:
        marnie = User(
            username='marnie',
            email='marnie@aa.io',
            password='password',
            first_name='Marnie',
            last_name='May',
            role='admin',
            created_at=now,
            updated_at=now
        )
    bobbie = User.query.filter_by(username='bobbie').first()
    if not bobbie:
        bobbie = User(
            username='bobbie',
            email='bobbie@aa.io',
            password='password',
            first_name='Bobbie',
            last_name='Smith',
            role='member',
            created_at=now,
            updated_at=now
        )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()