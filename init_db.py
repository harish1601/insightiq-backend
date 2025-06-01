from database import database
from models import user

database.Base.metadata.create_all(bind=database.engine)