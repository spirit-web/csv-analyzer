# Här hämtar vi strukturen och riktlinjer för databasens utforming. Kolumnerna och vad som får vara i dem.
from sqlalchemy import Column, Integer, String, DateTime
# Här hämtar vi en funktion som automatiskt generera tidsstämplar för observationer som användare lägger in
from sqlalchemy.sql import func
# Här hämtar vi den Base vi tidigare la in i database.py. Denna behövs när vi ska bygga class Observation(Base) så att vi kan översätta python klassen till databastabell.
from database import Base

# Här bygger vi en grundklass som ärvt base logik för att översätta python till databastabeller. 
# classen heter Observations. Databasen som skapas behöver ha ett eget namn som vi här kallar tablename
# Varje rad har ett unikt ID och primary key som gör att vi kan göra korrigeringar i just den raden även om 2 rader har samma namn. Index gör det lättare att söka i databasen. 
class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    filnamn = Column(String, nullable=False)
    anteckning = Column(String, nullable=False)
    skapad = Column(DateTime, default=func.now())
