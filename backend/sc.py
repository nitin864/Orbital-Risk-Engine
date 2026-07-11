from app.database.database import Base, engine
from app.database.models import SatelliteDB, CloseApproachDB

Base.metadata.create_all(bind=engine)
print("Tables recreated")