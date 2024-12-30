import requests
from bs4 import BeautifulSoup

def get_medicine_prospecto(nombre_medicamento):
    url = "https://cima.aemps.es/cima/rest/medicamentos"
    params = {"nombre": nombre_medicamento}
    
    response = requests.get(url, params=params)

    # Verifica si la respuesta es JSON válida
    try:
        medicamentos = response.json()
    except Exception as e:
        return None, f"Error al procesar la respuesta de la API: {e}"

    # Verificar si 'resultados' está presente en la respuesta
    if not medicamentos.get('resultados'):
        print("Respuesta inesperada de la API")
        print(medicamentos)
        return None, "No se encontraron medicamentos con ese nombre."

    # Lista completa de medicamentos usados para tratar glaucoma
    medicamentos_glaucoma = [
        "combigan", "xalatan", "travatan", "lumigan", "azopt", "alphagan",
        "cosopt", "pilocarpina", "betoptic", "timolol", "ganfort", "simbrinza",
        "trusopt", "fotil", "bimatoprost", "latanoprost", "dorzolamida", "brinzolamida",
        "tafluprost", "carteolol", "rescula", "istalol"
    ]

    # Extraer lista de medicamentos
    lista_medicamentos = medicamentos['resultados']

    # Recorrer medicamentos y buscar prospecto (tipo 2)
    for medicamento in lista_medicamentos:
        nombre = medicamento['nombre']
        nregistro = medicamento['nregistro']
        docs = medicamento.get('docs', [])

        # Buscar documento tipo 2 (Prospecto)
        prospecto_url = None
        for doc in docs:
            if doc['tipo'] == 2:  # Tipo 2 = Prospecto
                prospecto_url = doc.get('urlHtml')
                break

        if not prospecto_url:
            continue  # No mostrar medicamentos sin prospecto

        # Obtener el prospecto en HTML
        response = requests.get(prospecto_url)
        if response.status_code != 200:
            continue  # Saltar si no se puede acceder al prospecto

        # Extraer texto del prospecto usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        texto_prospecto = soup.get_text()

        # Verificar si el medicamento es usado para tratar glaucoma
        if any(med in nombre.lower() for med in medicamentos_glaucoma):
            resultado = f"{nombre}: ✅ Usado para tratar glaucoma"
        elif "glaucoma" in texto_prospecto.lower():
            resultado = f"{nombre}: ❌ Contraindicado para glaucoma"
        else:
            resultado = f"{nombre}: ✅ No contraindicado para glaucoma"

        # Formatear salida
        print("\n" + "="*50)
        print(f"\U0001F539 Medicamento: {nombre}")
        print(f"\U0001F538 Laboratorio: {medicamento['labtitular']}")
        print(f"\U0001F538 Vía de administración: {medicamento['viasAdministracion'][0]['nombre']}")
        print(f"\U0001F538 Forma farmacéutica: {medicamento['formaFarmaceutica']['nombre']}")
        print(f"\U0001F538 Dosis: {medicamento['dosis']}")
        print(f"\U0001F538 N° de Registro: {nregistro}")
        print(f"\U0001F538 Estado: {'Comercializado' if medicamento['comerc'] else 'No comercializado'}")
        print(f"\U0001F538 {resultado}")
        print(f"\U0001F517 Prospecto: {prospecto_url}")
        print("="*50 + "\n")

if __name__ == "__main__":
    medicamento = input("Introduce el nombre del medicamento: ")
    get_medicine_prospecto(medicamento)
