from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cruds.tournament_inscription_crud import (
    expel_user_from_tournament, get_tournament_inscriptions,
    get_tournament_inscriptions_by_user, get_user_tournament_inscriptions,
    inscribe_user_to_tournament)
from db.database import get_db
from schemas.tournament_inscription import (TournamentInscription,
                                            TournamentInscriptionCreate)

router = APIRouter(
    prefix="/tournament", tags=["inscriptions"], )


@router.post("/inscriptions/")
def inscribe_user(tournament_inscription: TournamentInscriptionCreate, tournament_id: int,  db: Session = Depends(get_db)):
    existing_inscriptions = get_tournament_inscriptions(db, tournament_id)
    for inscription in existing_inscriptions:
        if inscription.first_player == tournament_inscription.first_player or inscription.first_player == tournament_inscription.second_player:
            return {"message": "User is already inscribed in the tournament"}
        if inscription.second_player == tournament_inscription.first_player or inscription.second_player == tournament_inscription.second_player:
            return {"message": "User is already inscribed in the tournament"}
    inscribe_user_to_tournament(db, tournament_inscription, tournament_id)
    return {"message": "User has been inscribed to the tournament"}


@router.delete("/inscriptions/")
def expel_user(user_id: int, tournament_id: int, db: Session = Depends(get_db)):
    expel_user_from_tournament(db, user_id, tournament_id)
    return {"message": "User has been expelled from the tournament"}


@router.get("/inscriptions/{tournament_id}/", response_model=List[TournamentInscription])
def get_tournament_inscriptions_by_tournament(tournament_id: int, db: Session = Depends(get_db)):
    inscriptions = get_tournament_inscriptions(db, tournament_id)
    if not inscriptions:
        raise HTTPException(status_code=404, detail="Inscriptions not found")
    return inscriptions


@router.get("/inscriptions/users/{user_id}/", response_model=List[TournamentInscription])
def get_tournament_inscriptions_by_user(user_id: int, db: Session = Depends(get_db)):
    inscriptions = get_tournament_inscriptions_by_user(db, user_id)
    if not inscriptions:
        raise HTTPException(status_code=404, detail="Inscriptions not found")
    return inscriptions


@router.get("/inscriptions/users/me/", response_model=List[TournamentInscription])
def get_user_tournament_inscriptions(db: Session = Depends(get_db)):
    inscriptions = get_user_tournament_inscriptions(db)
    if not inscriptions:
        raise HTTPException(status_code=404, detail="Inscriptions not found")
    return inscriptions
