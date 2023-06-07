import database


def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


def post_db(db, data):
    db.add(data)
    db.commit()
    db.refresh(data)
