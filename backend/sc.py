from app.database.database import Base, engine
from app.database.models import CloseApproachDB

Base.metadata.create_all(bind=engine)
print("close_approaches table created")