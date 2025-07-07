import requests
import sys

API_KEY = "a2abec8b-3eda-4961-98fa-ee9bff26a98d"  # Reemplaza con tu API Key real

def obtener_coordenadas(ciudad):
    url = f"https://graphhopper.com/api/1/geocode"
    params = {
        'q': ciudad,
        'locale': 'es',
        'key': API_KEY
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()

    if datos['hits']:
        lat = datos['hits'][0]['point']['lat']
        lon = datos['hits'][0]['point']['lng']
        return lat, lon
    else:
        print(f"No se pudo encontrar la ciudad: {ciudad}")
        return None, None

def obtener_ruta(origen, destino, medio_transporte):
    lat_origen, lon_origen = obtener_coordenadas(origen)
    lat_destino, lon_destino = obtener_coordenadas(destino)

    if None in (lat_origen, lon_origen, lat_destino, lon_destino):
        print("Error al obtener coordenadas.")
        return

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{lat_origen},{lon_origen}", f"{lat_destino},{lon_destino}"],
        "vehicle": medio_transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'paths' not in data:
        print("ERROR: La respuesta no contiene 'paths'")
        print("Respuesta de la API:", data)
        return

    path = data['paths'][0]

    distancia_km = path['distance'] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_minutos = path['time'] / (1000 * 60)

    print(f"\n📍 Distancia: {distancia_km:.2f} km | {distancia_millas:.2f} millas")
    print(f"⏱️  Duración estimada: {duracion_minutos:.2f} minutos")

    print("\n🗺️  Instrucciones de ruta:")
    for paso in path['instructions']:
        print(f"➡️  {paso['text']} ({paso['distance']:.0f} m)")

# ======== Bucle principal ==========
while True:
    print("\nPresiona 's' para salir.")
    origen = input("Ciudad de origen: ")
    if origen.lower() == 's':
        sys.exit()

    destino = input("Ciudad de destino: ")
    if destino.lower() == 's':
        sys.exit()

    print("Opciones de transporte: car, bike, foot")
    medio = input("Medio de transporte: ")
    if medio.lower() == 's':
        sys.exit()

    obtener_ruta(origen, destino, medio)

