from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np

app = FastAPI()

# Cargar el modelo
modelo = joblib.load("modelo.pkl")

# Modelo de datos
class Persona(BaseModel):
    edad: int
    educacion: int
    horas_trabajadas: int

@app.post("/predecir-multiple")
def predecir_ingreso_multiple(personas: List[Persona]):
    # Convertir los objetos Persona a una matriz numpy
    datos = np.array([[p.edad, p.educacion, p.horas_trabajadas] for p in personas])

    # Hacer predicciones
    predicciones = modelo.predict(datos)

    # Generar respuesta
    resultados = []
    for persona, pred in zip(personas, predicciones):
        gana = bool(pred)
        resultados.append({
            "nombre": persona.__dict__,
            "gana_mas_de_50k": gana,
            "mensaje": "✅ Gana más de $50k" if gana else "❌ No gana más de $50k"
        })

    return {"predicciones": resultados}
