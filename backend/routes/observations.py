# APIRouter är en behållare för endpoints som vi sedan kan koppla till app.py
# Depends gör att man slipper skriva ut get_db()
# HTTPException behövs för att returnera felmeddelande såsom 404 Not Found
# status innehåller statuskoderna som färdiga konstanter. Istället för att skriva 201 så skriver vi status.HTTP_201_CREATED
from fastapi import APIRouter, Depends, HTTPException, status
# Session är datatypen för db variabeln
from sqlalchemy.orm import Session
# Denna används när en endpoint returnerar en lista av objekt
from typing import List
# get_db är som nyckeln till kylskåpet (databasen)
# db är databassessionen som är som själva nyckeln till databasen som Depends ger automatiskt
from database import get_db
# hämtar SQLAlchemy klassen Observation för att endpoint ska kunna göra db.query(Observation)
from models.observation import Observation
# Hämtar Pydantic klasserna för både in och ut valideringen
from schemas.observation import ObservationCreate, ObservationResponse

# prefix="/observations" gör att alla endpoints automatiskt från /observations framför sig
# tags grupperar endpoints för att göra dem lätta att hitta
router = APIRouter(prefix="/observations", tags=["observations"])

# @ är som en etikett vad paketet är till för. Den här funktionen svarar på POST request
# data: ObservationCreate är det frontend skickar in där Pydantic validerar så att filnamn och anteckningar ej är tomma
# Här byggs själv objektet från ritningen men är ej sparad i databasen ännu
# db.add lägger objektet i kön för att sparas men ännu ej sparat
# db.commit gör att objektet sparas i databasen
# Hämtar det sparade objektet från databasen som nu fått id och skapad ifyllda från databasen
# Hämtar det sparade objektet från databasen som nu fått id och skapad ifyllda från databasen
# Med return skickas objektet tillbaka till frontend

@router.post("/", response_model=ObservationResponse, status_code=status.HTTP_201_CREATED)
def create_observation(data: ObservationCreate, db: Session = Depends(get_db)):
    obs = Observation(filnamn=data.filnamn, anteckning=data.anteckning)
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

# Nu gör vi en GET istället för POST för att vi vill hämta data iform av en lista av objekt istället för att skapa ett objekt
# def get_observations utför funktionen att hämta datan

@router.get("/", response_model=List[ObservationResponse])
def get_observations(db: Session = Depends(get_db)):
    return db.query(Observation).all()

# GET /observations/{id} hämtar en specifik observation via dess ID och returnerar fel om den inte finns
@router.get("/{id}", response_model=ObservationResponse)
def get_observation(id: int, db: Session = Depends(get_db)):
    obs = db.query(Observation).filter(Observation.id == id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observation hittades inte")
    return obs

# PUT ändrar specifik observation via ID samt skickar felmeddelande om ej hittar. Ändrar filnamn och anteckningar i databasen till det som användaren skriver in. 
# commit() sparar ändringen och refresh återger den nya uppdaterade
@router.put("/{id}", response_model=ObservationResponse)
def update_observation(id: int, data: ObservationCreate, db: Session = Depends(get_db)):
    obs = db.query(Observation).filter(Observation.id == id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observation hittades inte")
    obs.filnamn     = data.filnamn
    obs.anteckning  = data.anteckning
    db.commit()
    db.refresh(obs)
    return obs

# DELETE söker upp ett objekt med en observation via ID numret och tar bort den samt anger statuskod 204 No Content där ingen data skickas tillbaka eller 404 hittades inte
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_observation(id: int, db: Session = Depends(get_db)):
    obs = db.query(Observation).filter(Observation.id == id).first()
    if not obs:
        raise HTTPException(status_code=404, detail="Observation hittades inte")
    db.delete(obs)
    db.commit()
