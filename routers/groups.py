from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

from cruds.tournament_crud import get_tournament
from db.database import get_db
from models.group import GroupModel
from models.tournament_inscription_model import TournamentInscriptionModel
from schemas.group import Group, GroupCreate
from schemas.group_with_inscriptions import (GroupWithInscriptions,
                                             TournamentWithGroupInscriptions)
from schemas.tournament_inscription import TournamentInscription

router = APIRouter(
    prefix="/tournament", tags=["groups"], )


@router.post("/group/{group_id}/inscription")
async def assign_inscription(group_id: int, inscription_id: int, db: Session = Depends(get_db)):
    inscription = db.query(TournamentInscriptionModel).filter_by(
        id=inscription_id).first()
    if inscription:
        group = db.query(GroupModel).filter_by(id=group_id).first()
        if group:
            inscription.group_id = group_id
            db.commit()
            return {"message": "Inscription assigned to group"}
        else:
            return {"message": "Group not found"}
    else:
        return {"message": "Inscription not found"}


@router.get("/group/{group_id}", response_model=GroupWithInscriptions)
async def get_group_with_inscriptions(group_id: int, db: Session = Depends(get_db)):
    group: GroupModel = db.query(GroupModel).filter_by(id=group_id).first()
    if group:
        inscriptions = sorted(
            group.inscriptions, key=lambda x: (x.position, x.updated_at))
        return {"group": group, "inscriptions": inscriptions}
    else:
        return {"message": "Group not found"}


@router.post("/group", response_model=Group)
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    new_group = GroupModel(**group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("/group/",)
async def get_groups_by_tournament_id(tournament_id: int, db: Session = Depends(get_db)):
    groups = db.query(GroupModel).filter_by(tournament_id=tournament_id).all()

    group_list = []
    for group in groups:
        inscriptions = group.inscriptions
        group_list.append({"id": group.id,
                           "tournament_id": group.tournament_id,
                           "group": group,
                           })

    return groups


@router.delete("/group/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(GroupModel).filter_by(id=group_id).first()
    if group:
        db.delete(group)
        db.commit()
        return {"message": "Group deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Group not found")


@router.put("/group/inscriptions/{inscription_id}")
def update_inscription(inscription_id: int, position: int, db: Session = Depends(get_db)):
    inscription = db.query(TournamentInscriptionModel).filter(
        TournamentInscriptionModel.id == inscription_id).first()

    if inscription:
        inscription.position = position
        inscription.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(inscription)
        return {"message": "Inscription updated successfully"}

    return {"message": "Inscription not found"}
