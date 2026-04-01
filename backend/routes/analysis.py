# ApiRouter är behållaren för endpoints
# UploadFile är en speciell FastAPI klass för att ta emot uppladdade filer som hanterar att läsa filinnehållet utan att spara datan
# File berättar för FastAPI att en parameter är en fil och inte en vanlig JSON data. Denna används tillsammans med UploadFile
# HTTPException används för att returnera felmeddelanden om något går fel
# import pandas as pd importerar pandas biblioteket och ger det förkortning pd. Ex. pd.read_csv() istället för pandas.read_csv().
# import io är ett inbyggt python bibliotek för att hantera data i minnet som om det va en fil. När FastAPI tar emot en uppladdad fil är innehållet binärt i 1or och 0or.
# io.BytesIO() omvandlar dessa 1or och 0or (bytes) till fil liknande objekt som pandas kan läsa direkt utan något behöver sparas på disken 
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

# Detta skapar routern med prefix /analysis där alla endpoints får /analysis framför sig
router = APIRouter(prefix="/analysis", tags=["analysis"])

# Denna tar emot en CSV fil och ger tillbara statistik som JSON
@router.post("/statistics")
async def analysera_csv(fil: UploadFile = File(...)):


    # Kontroll att filen sluter på .csv och returnerar 400 bad request om ej stämmer
    if not fil.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Endast CSV-filer stöds")
    
    # Läser filens innehåll som råa 1or och 0or från uppladdade filer
    innehall = await fil.read()

    # io.BytesIO omvandlar bytes till ett fil objekt som Pandas kan läsa
    # Detta gör så att pd förstår att det är en fil
    df = pd.read_csv(io.BytesIO(innehall))

    # Väljer ut kolumner med siffror 
    numeriska = df.select_dtypes(include="number")

    # Ger tillbaka felkod 400 om filen inte innehåller numeriska kolumner
    if numeriska.empty:
        raise HTTPException(status_code=400, detail="Inga numeriska kolumner hittades")
    
    # Själva rådata
    rader, kolumner     = df.shape
    alla_kolumner       = list(df.columns)
    datatyper           = df.dtypes.astype(str).to_dict()

    # Datareningen
    saknade_varden      = df.isnull().sum().to_dict()
    saknade_procent     = (df.isnull().mean() * 100).round(1).to_dict()
    duplikat            = int(df.duplicated().sum())

    # Identifiering av outliers
    outliers = {}
    for kolumn in numeriska.columns:
        Q1  = numeriska[kolumn].quantile(0.25)
        Q3  = numeriska[kolumn].quantile(0.75)
        IQR = Q3 - Q1
        antal = int(((numeriska[kolumn] < Q1 - 1.5 * IQR) |
                     (numeriska[kolumn] > Q3 + 1.5 * IQR)).sum())
        outliers[kolumn] = antal

    # Data analys
    describe            = numeriska.describe().round(3).to_dict()
    korrelationer       = numeriska.corr().round(3).to_dict()

    # Skickar tillbaka data som JSON där FastAPI omvandlar automatiskt
    return {
        "radata": {
            "rader":        rader,
            "kolumner":     kolumner,
            "namn":         alla_kolumner,
            "datatyper":    datatyper
        }, 
        "datarening":{
            "saknade_varden":   saknade_varden,
            "saknade_procent":  saknade_procent,
            "duplikat":         duplikat,
            "outliers":         outliers
        },
        "eda":  {
            "describe":         describe,
            "korrelationer":    korrelationer
        }
    }


