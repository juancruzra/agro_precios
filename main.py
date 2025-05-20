from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/precios")
def get_precios():
    url = "https://www.cac.bcr.com.ar/es/precios-de-pizarra"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tablas = soup.find_all("table")
    precios = []

    for tabla in tablas:
        rows = tabla.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > 1:
                producto = cols[0].get_text(strip=True)
                precio = cols[1].get_text(strip=True)
                precios.append({"producto": producto, "precio": precio})

    return {"precios": precios}
