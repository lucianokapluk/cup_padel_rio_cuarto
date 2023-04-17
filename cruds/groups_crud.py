from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.groups_model import GroupModel
from models.tournament_inscription_model import TournamentInscriptionModel
from schemas.groups import Group, GroupCreate, GroupUpdate

""" def create_group(db: Session, group: GroupCreate, tournament_id: int, inscription_id: int) -> GroupModel:
    db_group = GroupModel(
        tournament_id=tournament_id,
        group_number=group.group_number,
        inscription_id=inscription_id
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group
 """


def create_group(db: Session, group: GroupCreate, tournament_id: int, inscription_id: int) -> GroupModel:
    inscription = db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.id == inscription_id).first()
    db_group = GroupCreate(
        tournament_id=tournament_id,
        group_number=group.group_number,
        inscriptions=[inscription]
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_id: int):
    group = db.query(GroupModel).filter(GroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    groups = db.query(GroupModel).offset(skip).limit(limit).all()
    return groups


def update_group(db: Session, group_id: int, group: GroupUpdate):
    db_group = get_group(db, group_id)
    for field, value in group:
        setattr(db_group, field, value)
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int):
    db_group = get_group(db, group_id)
    db.delete(db_group)
    db.commit()
    return db_group
