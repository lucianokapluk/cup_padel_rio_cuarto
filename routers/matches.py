from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from db.database import Base, engine, get_db
from models.match_model import MatchModel
from models.tournament_inscription_model import TournamentInscriptionModel
from schemas.match import Match, MatchCreate, MatchUpdate

router = APIRouter(
    prefix="/tournament", tags=["Matches"], )


@router.post("/matches/", response_model=Match)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = MatchModel(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.get("/matches/{match_id}", response_model=Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(MatchModel).filter(
        MatchModel.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/matches/{match_id}", response_model=Match)
def update_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = db.query(MatchModel).filter(
        MatchModel.id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    for key, value in match.dict().items():
        setattr(db_match, key, value)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(MatchModel).filter(
        MatchModel.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(match)
    db.commit()
    return {"message": "Match deleted successfully"}


@router.get("/matches/user/{user_id}", response_model=list[Match])
def get_matches_by_user(user_id: int, db: Session = Depends(get_db)):
    matches = db.query(MatchModel).filter(
        (MatchModel.first_inscription_id == user_id) |
        (MatchModel.second_inscription_id == user_id)
    ).all()
    return matches


@router.get("/matches/", response_model=list[Match])
def list_matches(db: Session = Depends(get_db)):
    matches = db.query(MatchModel).all()
    return matches


@router.get("/matches/user/{user_id}/won", response_model=dict)
def get_matches_won_by_user(user_id: int, db: Session = Depends(get_db)):
    matches_won = db.query(func.count()).\
        select_from(MatchModel).\
        join(TournamentInscriptionModel,
             MatchModel.winer == TournamentInscriptionModel.id).\
        filter(or_(
            TournamentInscriptionModel.first_player_id == user_id,
            TournamentInscriptionModel.second_player_id == user_id
        )).scalar()

    matches_lost = db.query(func.count()).\
        select_from(MatchModel).\
        join(TournamentInscriptionModel,
             MatchModel.winer != TournamentInscriptionModel.id).\
        filter(or_(
            TournamentInscriptionModel.first_player_id == user_id,
            TournamentInscriptionModel.second_player_id == user_id
        )).filter(or_(
            MatchModel.first_inscription_id == TournamentInscriptionModel.id,
            MatchModel.second_inscription_id == TournamentInscriptionModel.id
        )).scalar()
    matches_played = db.query(func.count()).\
        select_from(MatchModel).\
        join(TournamentInscriptionModel,
             or_(
                 MatchModel.first_inscription_id == TournamentInscriptionModel.id,
                 MatchModel.second_inscription_id == TournamentInscriptionModel.id
             )).\
        filter(or_(
            TournamentInscriptionModel.first_player_id == user_id,
            TournamentInscriptionModel.second_player_id == user_id
        )).scalar()
    return {"matches_won": matches_won, "matches_lost": matches_lost,   "matches_played": matches_played}
