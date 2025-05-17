import requests

# URL de la API local
url = "http://localhost:8000/predecir-ingreso"

# Recolectar datos del usuario
def pedir_datos():
    
    edad = int(input("Edad: "))
    educacion = int(input("Años de educación formal: "))
    horas = int(input("Horas trabajadas por semana: "))
        
    persona ={
            "edad": edad,
            "educacion": educacion,
            "horas_trabajadas": horas
        }

    return persona

# Enviar los datos a la API
def hacer_prediccion(data):
    response = requests.post(url, json=data)
    print(response)

    if response.status_code == 200:
        resultados = response.json()

        print("\n📊 Resultados:")
        
        print(f"Persona: {resultados['mensaje']}")
    else:
        print("❌ Error al comunicarse con la API:", response.status_code)

# Programa principal
if __name__ == "__main__":
    datos = pedir_datos()
    hacer_prediccion(datos)
