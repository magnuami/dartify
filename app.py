from fastapi import FastAPI, Depends, Request, Form, status, Header, HTTPException
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models.models as models
from services import db_service as dbs
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def players(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    context = {"request": request}
    return templates.TemplateResponse("home/index.html", context)

@app.get("/players")
def players(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    players = dbs.get_players(db)
    context = {"request": request, 'players': players}
    return templates.TemplateResponse("players/players.html", context)

@app.post("/players/add")
def add_player(request: Request, hx_request: Optional[str] = Header(None), name: str = Form(...), db: Session = Depends(get_db)):
    player = dbs.get_player(db, name)
    if player: 
        raise HTTPException(status_code=400, detail="Player already registered")
    dbs.add_player(db, name)
    players = dbs.get_players(db)
    context = {"request": request, 'players': players}
    if hx_request:
        return templates.TemplateResponse("players/partials/table.html", context) 
    url = app.url_path_for("players")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.post("/players/delete/{player_id}")
def delete(request: Request, player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player: 
        raise HTTPException(status_code=400, detail="Player not found")
    db.delete(player)
    db.commit()
    
    # return partial 
    url = app.url_path_for("players")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get("/games")
def games(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    context = {"request": request}
    return templates.TemplateResponse("games/games.html", context)

@app.get("/leagues")
def leagues(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    players = dbs.get_players(db)
    context = {"request": request, 'players': players}  
    return templates.TemplateResponse("leagues/leagues.html", context)

@app.post("/leagues/create")
def create_league(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    players = dbs.get_players(db)
    context = {"request": request, 'players': players}  
    return

@app.post("/games/generate")
def create_league(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)): 
    return
    

