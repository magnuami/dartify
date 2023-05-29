from sqlalchemy.orm import Session

from schema.schema import Player
from models import models

def get_player(db: Session, player_name: str):
    return db.query(models.Player).filter(models.Player.name == player_name).first()

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def add_player(db: Session, player_name: str):
    new_player = models.Player(name=player_name)
    db.add(new_player)
    db.commit()