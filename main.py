from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Cargar el modelo entrenado
modelo = joblib.load("modelo.pkl")

app = FastAPI()

class Persona(BaseModel):
    edad: int
    educacion: int  # años de estudios
    horas_trabajadas: int

@app.post("/predecir-ingreso")
def predecir_ingreso(persona: Persona):
    datos = np.array([[persona.edad, persona.educacion, persona.horas_trabajadas]])
    prediccion = modelo.predict(datos)
    gana_mas = bool(prediccion[0])
    return {
        "gana_mas_de_50k": gana_mas,
        "mensaje": "✅ Gana más de $50k" if gana_mas else "❌ No gana más de $50k"
    }
