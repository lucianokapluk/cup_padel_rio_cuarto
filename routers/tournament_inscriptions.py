from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cruds.tournament_crud import get_tournaments
from cruds.tournament_inscription_crud import (
    expel_user_from_tournament, get_tournament_inscriptions,
    get_tournament_inscriptions_by_user, get_user_tournament_inscriptions,
    inscribe_user_to_tournament)
from db.database import get_db
from models.tournament_inscription_model import TournamentInscriptionModel
from schemas.tournament_inscription import (TournamentInscription,
                                            TournamentInscriptionCreate)

router = APIRouter(
    prefix="/tournament", tags=["inscriptions"], )


@router.post("/inscriptions/")
def inscribe_user(tournament_inscription: TournamentInscriptionCreate, tournament_id: int,  db: Session = Depends(get_db)):
    existing_inscriptions = get_tournament_inscriptions(db, tournament_id)
    for inscription in existing_inscriptions:
        if inscription.first_player_id == tournament_inscription.first_player_id or inscription.first_player_id == tournament_inscription.second_player_id:
            return {"message": "User is already inscribed in the tournament"}
        if inscription.second_player == tournament_inscription.first_player_id or inscription.second_player_id == tournament_inscription.second_player_id:
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
    filtered_inscriptions = [
        inscription for inscription in inscriptions if inscription.group_id is None]
    if not filtered_inscriptions:
        raise HTTPException(
            status_code=404, detail="Inscriptions without group_id not found")
    return filtered_inscriptions


@router.get("/inscriptions/users/{user_id}/", response_model=List[TournamentInscription])
def get_tournament_inscriptions_by_user_id(user_id: int, db: Session = Depends(get_db)):

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


@router.put("/inscriptions/{inscription_id}/group_id", response_model=TournamentInscription)
def update_tournament_inscription_group_id_endpoint(
    inscription_id: int, db: Session = Depends(get_db)
):
    inscription = get_tournament_inscription(db, inscription_id)
    if not inscription:
        raise HTTPException(status_code=404, detail="Inscription not found")

    updated_inscription = update_tournament_inscription_group_id(
        db, inscription_id)
    return updated_inscription


def get_tournament_inscription(db: Session, inscription_id: int) -> TournamentInscription:
    return db.query(TournamentInscriptionModel).filter(TournamentInscriptionModel.id == inscription_id).first()


def update_tournament_inscription_group_id(
    db: Session, inscription_id: int
) -> TournamentInscription:
    inscription = get_tournament_inscription(db, inscription_id)
    if not inscription:
        return None

    inscription.group_id = None
    inscription.position = None
    db.commit()
    db.refresh(inscription)
    return inscription
