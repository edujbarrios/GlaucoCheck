# GlaucoCheck - Detección de medicamentos contraindicados para glaucoma

## WEB APP LINK: [https://glaucocheck.streamlit.app/](https://glaucocheck.streamlit.app/)

## Descripción
GlaucoCheck es una aplicación web desarrollada con Streamlit que permite verificar si un medicamento está contraindicado para pacientes con glaucoma. A través de la API de CIMA (Centro de Información de Medicamentos de la AEMPS), se obtiene información actualizada sobre medicamentos y sus prospectos.

La aplicación resalta si un medicamento:
- **Está contraindicado para glaucoma** (indicado en rojo)
- **Es usado para tratar glaucoma** (indicado en verde oscuro)
- **No está contraindicado para glaucoma** (indicado en azul oscuro)

## Justificación
El glaucoma es una condición oftalmológica que puede agravarse con ciertos medicamentos. Esta aplicación ofrece una herramienta útil para profesionales de la salud y pacientes, ayudando a identificar rápidamente medicamentos que pueden afectar negativamente la condición del paciente.

## Características
- **Búsqueda por nombre de medicamento**
- **Resultados visuales claros** para indicar el estado del medicamento respecto al glaucoma
- **Enlaces directos al prospecto del medicamento**
- **Interfaz simple y rápida**

## Requisitos
- Python 3.8 o superior
- Streamlit
- Requests
- BeautifulSoup4
