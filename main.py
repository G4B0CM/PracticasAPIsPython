from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
import joblib

# 🔐 Configuración
SECRET_KEY = "tu_clave_super_secreta"
ALGORITHM = "HS256"

# Usuario de prueba (ideal usar base de datos en producción)
fake_user = {
    "username": "admin",
    "hashed_password": "$2b$12$ZQ1IpaEgUtrUIQkwhGcfw.l8mYHcwQ4LZgUYoUVbkUomRUuy4HPpW"  # contraseña: "admin123"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Modelo ML
modelo = joblib.load("modelo.pkl")

class Persona(BaseModel):
    edad: int
    educacion: int
    horas_trabajadas: int

class Resultado(BaseModel):
    predicciones: List[dict]

def verificar_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def autenticar_usuario(username, password):
    if username == fake_user["username"] and verificar_password(password, fake_user["hashed_password"]):
        return {"username": username}
    return None

def crear_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# 🔐 Ruta de login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token(user)
    return {"access_token": token, "token_type": "bearer"}

# 🔒 Ruta protegida
@app.post("/predecir-multiple", response_model=Resultado)
def predecir_multiple(datos: List[Persona], token: dict = Depends(verificar_token)):
    entradas = [[p.edad, p.educacion, p.horas_trabajadas] for p in datos]
    predicciones = modelo.predict(entradas)

    resultados = []
    for i, p in enumerate(predicciones):
        mensaje = "✅ Gana más de $50k" if p == 1 else "❌ No gana más de $50k"
        resultados.append({"persona": i + 1, "mensaje": mensaje})

    return {"predicciones": resultados}
