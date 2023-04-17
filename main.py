from fastapi import FastAPI

from db.database import Base, SessionLocal, engine
from models.category_model import Base
from models.group import Base
from models.ranking_model import Base
from models.tournament_inscription_model import Base
from models.tournament_model import Base
from models.user_model import Base
from routers import (category, groups, tournament, tournament_inscriptions,
                     users)

Base.metadata.create_all(bind=engine)

app = FastAPI()


# routers

app.include_router(users.router)
app.include_router(category.router)
app.include_router(tournament.router)
app.include_router(tournament_inscriptions.router)
app.include_router(groups.router)
