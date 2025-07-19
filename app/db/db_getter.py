from app.db.mongo import MongoDB
from app.settings import get_settings
#Get and return MongoDB database
def get_db():
    settings = get_settings()
    return MongoDB(settings).db
