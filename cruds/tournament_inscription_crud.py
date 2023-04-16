from typing import List

from sqlalchemy.orm import Session

from models.tournament_inscription_model import TournamentInscriptionModel
from schemas.tournament_inscription import TournamentInscriptionCreate


def inscribe_user_to_tournament(db: Session, inscription: TournamentInscriptionCreate, tournament_id: int):
    tournament_inscription = TournamentInscriptionModel(
        **inscription.dict(), tournament_id=tournament_id)
    db.add(tournament_inscription)
    db.commit()
    db.refresh(tournament_inscription)
    return tournament_inscription


def expel_user_from_tournament(db: Session, user_id: int, tournament_id: int):
    db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.first_player == user_id,
        TournamentInscriptionModel.tournament_id == tournament_id
    ).delete()
    db.commit()


def get_tournament_inscriptions(db: Session, tournament_id: int) -> List[TournamentInscriptionModel]:
    inscriptions = db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.tournament_id == tournament_id
    ).all()
    return inscriptions


def get_tournament_inscriptions_by_user(db: Session, user_id: int) -> List[TournamentInscriptionModel]:
    inscriptions = db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.first_player == user_id
    ).all()
    return inscriptions


def get_user_tournament_inscriptions(db: Session, user_id: int) -> List[TournamentInscriptionModel]:
    inscriptions = db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.first_player == user_id
    ).all()
    return inscriptions
