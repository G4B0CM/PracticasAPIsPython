# guardar_modelo.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Datos de ejemplo
data = pd.DataFrame({
    "edad": [25, 40, 35, 50],
    "educacion": [12, 16, 14, 18],  # años de educación formal
    "horas_trabajadas": [40, 50, 45, 60],
    "gana_mas_50k": [0, 1, 0, 1]
})

X = data[["edad", "educacion", "horas_trabajadas"]]
y = data["gana_mas_50k"]

modelo = RandomForestClassifier()
modelo.fit(X, y)

# Guardar modelo
joblib.dump(modelo, "modelo.pkl")
