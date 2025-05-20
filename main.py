from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/precios")
def get_precios():
    url = "https://www.cac.bcr.com.ar/es/precios-de-pizarra"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Busca la tabla con clase específica (puede cambiar si modifican el diseño)
    tabla = soup.find("table", class_="table")

    if not tabla:
        return {"error": "No se encontró la tabla de precios"}

    rows = tabla.find_all("tr")
    precios = []

    for row in rows[1:]:  # Ignoramos la cabecera
        cols = row.find_all("td")
        if len(cols) >= 3:
            producto = cols[0].get_text(strip=True)
            entrega = cols[1].get_text(strip=True)
            precio = cols[2].get_text(strip=True)
            precios.append({
                "producto": producto,
                "entrega": entrega,
                "precio": precio
            })

    return {"fuente": url, "precios": precios}
