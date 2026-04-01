# CSV Analyzer program - Spirit Rosenberg

## Om projektet
En fullstack-applikation för att spara observationer och analysera CSV-data.
Byggd med FastAPI (backend) och React (frontend).

## Starta backend
cd backend
pip install -r requirements.txt
python app.py

## Starta frontend
cd frontend
npm install
npm run dev

## Endpoints

### Observationer
- POST   /observations        Skapa ny observation
- GET    /observations        Hämta alla observationer
- GET    /observations/{id}   Hämta en observation
- PUT    /observations/{id}   Uppdatera observation
- DELETE /observations/{id}   Ta bort observation

### Analys
- POST   /analysis/statistics   Ladda upp CSV och få statistik
- POST   /analysis/histogram    Ladda upp CSV och få histogram som bild