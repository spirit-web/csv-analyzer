# SQLalchemy är ett externt bibliotek vi hämtat via pip till requirements
# SQLalchemy gör att python kan översättas till SQL databas språk 
# create_engine är en motor som driver kommunikationen mellan Python och databasen
# SQLalchemy.ext.declarative innebär att vi går in djupare 2 gånger i bilioteket för att hämta något specifikt
# base är en grundklass där vi ärver SQLalchemys grundmall för databastabeller med all logik så att vi inte behöver skriva detta själva
# .orm står för Object Relational Mapper som är den del som översätter Python till SQL
# sessionmaker skapar en fabrik för databasessioner så att endpoints kan prata med databasen vid behov 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL är en konstant variabel som pekar på Kylskåpet där databasen ligger
DATABASE_URL = "sqlite:///./observations.db"

# engine är variabeln som gör att vi i andra moduler kan anropa till databasen
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Kaffebryggaren där SessionLocal är en bryggare och varje session är en kopp kaffe som bryggs när någon behöver den
# (autocommit=False, autoflush=False, bind=engine) är inställgningar för kaffebryggaren som anger att bl.a. inte spara till databasen automatiskt
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base är ett objekt som skapas av funktionen declarative_base()
# Detta objekt kommer vi kunna använda för att skapa class Observation(Base) med
Base = declarative_base()

#
# Med db = SessionLocal() brygger vi en kopp kaffe (skapar en ny databassession)
# try är en kontrollfunktion för att förebygga att programmet crashar
# yield används istället för return för att kunna invänta att enpointen gör klart sin request till databasen
# finally: db.close() stänger sedan sessionen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
