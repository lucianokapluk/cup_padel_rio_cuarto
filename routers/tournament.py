from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from cruds import tournament_crud
from db.database import SessionLocal, get_db
from schemas.tournament import Tournament, TournamentCreate, TournamentUpdate

router = APIRouter(
    prefix="/tournament", tags=["tournaments"], )
# Dependency


@router.post("/", response_model=Tournament)
def create_tournament_endpoint(tournament: TournamentCreate, db: Session = Depends(get_db)):
    db_tournament = tournament_crud.create_tournament(db, tournament)
    return db_tournament


@router.get("/{tournament_id}", response_model=Tournament)
def read_tournament(tournament_id: int, db: Session = Depends(get_db)):
    db_tournament = tournament_crud.get_tournament(db, tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament


@router.get("/", response_model=List[Tournament])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tournaments = tournament_crud.get_tournaments(db, skip=skip, limit=limit)
    return tournaments


@router.put("/{tournament_id}", response_model=Tournament)
def update_tournament_endpoint(tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)):
    db_tournament = tournament_crud.update_tournament(
        db, tournament_id, tournament)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament


@router.delete("/{tournament_id}")
def delete_tournament_api(tournament_id: int, db: Session = Depends(get_db)):
    tournament = tournament_crud.get_tournament(
        db, tournament_id=tournament_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    tournament_crud.delete_tournament(db, tournament_id)
    return {"detail": "Tournament deleted"}
