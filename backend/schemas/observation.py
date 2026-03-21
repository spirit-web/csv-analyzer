# BaseModel validerar att datan som går in och ut via API:et är rätt
from pydantic import BaseModel, Field
# Optional används när ett fält inte är obligatoriskt 
from typing import Optional 
# datetime behövs för tidsstämpeln skapad fältet för att auto registrera observationer
from datetime import datetime

# En klass ObservationCreate som ärver BaseModel från pydantic med förmåga att validera att rätt info går in
class ObservationCreate(BaseModel):
    filnamn:    str = Field(..., min_length=1)
    anteckning: str = Field(..., min_length=1)

# En klass ObservationResponse som ärver filnamn och antecknings villkoren från ObservationCreate classen så att dessa ej behöver skrivas ut igen
class ObservationResponse(ObservationCreate):
    id:     int
    skapad: datetime

    class Config:
        from_attributes = True

