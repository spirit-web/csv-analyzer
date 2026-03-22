# FastAPI är hela resturangen som de olka routers avdelningar kopplas till
from fastapi import FastAPI
# hämtar middleware som säkerhets checkar alla HTTP request och responses. Den låter React prata med FastAPI 
from fastapi.middleware.cors import CORSMiddleware
# hämtar Base och engine som är grundlassen och motorn från database.py. Dessa behövs för att skapa databastabellerna automatiskt
from database import engine, Base
# hämtar routern från observations.py och döper om den till observations_router för att namnet ska va tydligt när den kopplas till appen
from routes.observations import router as observations_router

# Base.metadata håller information om alla klasser som ärver från Base vilket i detta fallet blir Observation classen
# create_all() skapar alla tabeller som inte finns ännu. 
# bind=engine gör att vi kan använda motorn
# Hela den här raden är viktig för att skapa observations.db filen första gången programmet körs
Base.metadata.create_all(bind=engine)

# app är hela servern som tar emot alla request och skickar tillbaka responses. Och som är döpt till CSV Analyzer
# allow origins anger att bara React via denna addressen får prata med backend
# allow methods tillåter alla HTTP metoder - GET, POST, PUT, DELETE
# allow headers tillåter alla headers
app = FastAPI(title="CSV Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# denna kodrad kopplar alla endpoints från observations.py till appen.
# uvicorn.run gör så att servern går att starta med python app.py
app.include_router(observations_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)