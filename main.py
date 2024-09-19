import json
import os
from datetime import datetime

def load_data():
    try:
        if os.path.exists('pacientes.json'):
            with open('pacientes.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        return {"pacientes": []}
    except json.JSONDecodeError:
        print("Error: No se pudo leer el archivo 'pacientes.json'. El archivo está dañado.")
        return {"pacientes": []}

def save_data(data):
    try:
        with open('pacientes.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError:
        print("Error: No se pudo guardar los datos en 'pacientes.json'.")

def seleccionar_paciente(data):
    while True:
        try:
            print("\n1. Introducir nuevo paciente")
            print("2. Seleccionar paciente existente")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Introduzca el nombre del nuevo paciente: ")
                data["pacientes"].append({"nombre": nombre, "consultas": [], "clasificacion": "Clase A"})
                save_data(data)
                return nombre
            elif opcion == "2":
                if not data["pacientes"]:
                    print("No hay pacientes registrados.")
                    continue
                for i, paciente in enumerate(data["pacientes"], 1):
                    print(f"{i}. {paciente['nombre']}")
                seleccion = int(input("Seleccione el número del paciente: ")) - 1
                return data["pacientes"][seleccion]["nombre"]
            else:
                print("Opción no válida. Por favor, seleccione 1 o 2.")
        except (ValueError, IndexError):
            print("Error: Opción no válida. Por favor, seleccione un número de la lista.")

def evaluar_riesgo(diagnostico):
    alto_riesgo = [
        "infarto", "cáncer terminal", "insuficiencia respiratoria", "coma", 
        "hipertensión", "presión arterial elevada", "diabetes avanzada", 
        "fallo renal", "trombos", "embolia", "enfermedad cardiovascular grave"
    ]
    for riesgo in alto_riesgo:
        if riesgo in diagnostico.lower():
            return "Clase B"
    return "Clase A"

def nueva_consulta(paciente, data):
    try:
        consulta = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "motivo": input("Motivo de la visita: "),
            "historial": input("Historial clínico: "),
            "notas": input("Notas adicionales: "),
            "diagnostico": input("Diagnóstico: ")
        }

        riesgo = evaluar_riesgo(consulta["diagnostico"])
        consulta["riesgo"] = riesgo

        for p in data["pacientes"]:
            if p["nombre"] == paciente:
                p["consultas"].append(consulta)
                p["clasificacion"] = riesgo  
                break
        save_data(data)
    except Exception as e:
        print(f"Error al registrar la consulta: {e}")

def ver_consultas(paciente, data):
    try:
        for p in data["pacientes"]:
            if p["nombre"] == paciente:
                if not p["consultas"]:
                    print(f"\nNo hay consultas registradas para {paciente}.")
                    return

                print(f"\nConsultas anteriores para {paciente}:")
                for i, consulta in enumerate(p["consultas"], 1):
                    print(f"\nConsulta {i}:")
                    print(f"Fecha: {consulta['fecha']}")
                    print(f"Motivo: {consulta['motivo']}")
                    print(f"Historial: {consulta['historial']}")
                    print(f"Notas: {consulta['notas']}")
                    print(f"Diagnóstico: {consulta['diagnostico']}")
                    riesgo = consulta.get("riesgo", "No evaluado")
                    print(f"Riesgo: {riesgo}")
    except Exception as e:
        print(f"Error al ver las consultas: {e}")

def ver_clasificacion(paciente, data):
    try:
        for p in data["pacientes"]:
            if p["nombre"] == paciente:
                print(f"\nClasificación del paciente {paciente}: {p['clasificacion']}")
                break
    except Exception as e:
        print(f"Error al ver la clasificación: {e}")

def main():
    data = load_data()
    while True:
        try:
            paciente = seleccionar_paciente(data)
            while True:
                print(f"\nPaciente: {paciente}")
                print("1. Nueva consulta")
                print("2. Ver consultas anteriores")
                print("3. Ver clasificación del paciente")
                print("4. Cambiar de paciente")
                print("5. Salir")
                opcion = input("Seleccione una opción: ")

                if opcion == "1":
                    nueva_consulta(paciente, data)
                elif opcion == "2":
                    ver_consultas(paciente, data)
                elif opcion == "3":
                    ver_clasificacion(paciente, data)
                elif opcion == "4":
                    break
                elif opcion == "5":
                    print("Saliendo del programa.")
                    return
                else:
                    print("Opción no válida. Intente de nuevo.")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
