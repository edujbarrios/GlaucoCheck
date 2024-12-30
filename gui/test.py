import requests
from bs4 import BeautifulSoup
import streamlit as st

# Configuración de la aplicación
st.set_page_config(page_title="Glaucoma Medicamentos", page_icon="🩺")
st.title("🔍 App para determinar si un medicamento está contraindicado para glaucoma")

# Lista completa de medicamentos usados para tratar glaucoma
medicamentos_glaucoma = [
    "combigan", "xalatan", "travatan", "lumigan", "azopt", "alphagan",
    "cosopt", "pilocarpina", "betoptic", "timolol", "ganfort", "simbrinza",
    "trusopt", "fotil", "bimatoprost", "latanoprost", "dorzolamida", "brinzolamida",
    "tafluprost", "carteolol", "rescula", "istalol"
]

# Función para obtener el prospecto del medicamento
def get_medicine_prospecto(nombre_medicamento):
    url = "https://cima.aemps.es/cima/rest/medicamentos"
    params = {"nombre": nombre_medicamento}
    
    response = requests.get(url, params=params)

    try:
        medicamentos = response.json()
    except Exception as e:
        st.error(f"Error al procesar la respuesta de la API: {e}")
        return

    if not medicamentos.get('resultados'):
        st.warning("No se encontraron medicamentos con ese nombre.")
        return

    lista_medicamentos = medicamentos['resultados']

    for medicamento in lista_medicamentos:
        nombre = medicamento['nombre']
        nregistro = medicamento['nregistro']
        docs = medicamento.get('docs', [])

        prospecto_url = None
        for doc in docs:
            if doc['tipo'] == 2:
                prospecto_url = doc.get('urlHtml')
                break

        if not prospecto_url:
            continue

        response = requests.get(prospecto_url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        texto_prospecto = soup.get_text()

        if any(med in nombre.lower() for med in medicamentos_glaucoma):
            resultado = f"<div style='background-color:#155724; padding:15px; border-radius:8px; color:#d4edda; font-weight:bold;'>✅ Usado para tratar glaucoma</div>"
        elif "glaucoma" in texto_prospecto.lower():
            resultado = f"<div style='background-color:#721c24; padding:15px; border-radius:8px; color:#f8d7da; font-weight:bold;'>❌ Contraindicado para glaucoma</div>"
        else:
            resultado = f"<div style='background-color:#0c5460; padding:15px; border-radius:8px; color:#d1ecf1; font-weight:bold;'>✅ No contraindicado para glaucoma</div>"

        st.markdown("""
        ---
        #### Medicamento: {}
        **Laboratorio:** {}  
        **Vía de administración:** {}  
        **Forma farmacéutica:** {}  
        **Dosis:** {}  
        **N° de Registro:** {}  
        **Estado:** {}  
        {}  
        <a href="{}" target="_blank" style="display:block; margin-top:10px; background-color:#007bff; padding:10px; border-radius:5px; text-align:center; color:white; text-decoration:none; font-weight:bold;">📄 Ver Prospecto</a>
        """.format(
            nombre,
            medicamento['labtitular'],
            medicamento['viasAdministracion'][0]['nombre'],
            medicamento['formaFarmaceutica']['nombre'],
            medicamento['dosis'],
            nregistro,
            'Comercializado' if medicamento['comerc'] else 'No comercializado',
            resultado,
            prospecto_url
        ), unsafe_allow_html=True)

# Interfaz de entrada para el usuario
medicamento = st.text_input("Introduce el nombre del medicamento:")
if st.button("Buscar Medicamento"):
    if medicamento:
        get_medicine_prospecto(medicamento)
    else:
        st.warning("Por favor, introduce un nombre de medicamento.")

# Footer personalizado
st.markdown("""
---
📄 Made with ❤️ by [edujbarrios.com](https://www.edujbarrios.com)
""")
