from database import SessionDatabase


def get_db():
    db = SessionDatabase()
    try:
        yield db
    finally:
        db.close()

