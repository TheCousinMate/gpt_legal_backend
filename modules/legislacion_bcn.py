from fastapi import APIRouter, Query, HTTPException
import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from utils_output import output_dual, create_error_response
import re
import time
from urllib.parse import quote_plus

router = APIRouter(prefix="/legislacion")

DEFAULT_HEADERS = {
    "User-Agent": "ForensicLegalBot/4.1 (Chilean Legal Analysis Tool)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CL,es;q=0.8,en;q=0.6",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}
DEFAULT_TIMEOUT = 15

def parse_html_bcn(html: str, url: str = "") -> dict:
    """Extrae información legal desde HTML de BCN con análisis mejorado"""
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        # Extraer título con múltiples estrategias
        titulo = "Sin título"
        for selector in ["h1", ".titulo-norma", ".titulo-ley", "title"]:
            titulo_elem = soup.select_one(selector)
            if titulo_elem and titulo_elem.get_text(strip=True):
                titulo = titulo_elem.get_text(strip=True)
                break
        
        # Limpiar título
        titulo = re.sub(r'^(Ley Chile\s*-\s*)?', '', titulo)
        titulo = re.sub(r'\s+', ' ', titulo).strip()
        
        # Extraer fecha de publicación
        fecha = "Fecha no disponible"
        for selector in [".fecha-publicacion", ".fecha", "[class*='fecha']"]:
            fecha_elem = soup.select_one(selector)
            if fecha_elem:
                fecha = fecha_elem.get_text(strip=True)
                break
        
        # Si no encuentra fecha, buscar en texto
        if fecha == "Fecha no disponible":
            fecha_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+de\s+\w+\s+de\s+\d{4})'
            fecha_match = re.search(fecha_pattern, html)
            if fecha_match:
                fecha = fecha_match.group(1)
        
        # Extraer contenido/resumen
        contenido = "Contenido no disponible"
        
        # Estrategias múltiples para contenido
        content_selectors = [
            ".contenido-norma", ".resumen", ".extracto", 
            ".texto-norma", "article", ".content", "main"
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Limpiar texto
                for script in content_elem(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                
                text = content_elem.get_text(strip=True)
                if len(text) > 50:  # Contenido mínimo significativo
                    contenido = text[:500] + "..." if len(text) > 500 else text
                    break
        
        # Si no encuentra contenido específico, usar primeros párrafos
        if contenido == "Contenido no disponible":
            paragraphs = soup.find_all("p")
            if paragraphs:
                texto_parrafos = " ".join([p.get_text(strip=True) for p in paragraphs[:3] if p.get_text(strip=True)])
                if texto_parrafos:
                    contenido = texto_parrafos[:400] + "..." if len(texto_parrafos) > 400 else texto_parrafos
        
        # Generar ID si no se proporciona
        id_norma = extract_id_from_url(url) or generate_id_from_title(titulo)
        
        return {
            "id": id_norma,
            "titulo": titulo,
            "fecha_publicacion": fecha,
            "resumen": contenido,
            "url_fuente": url,
            "metadatos": {
                "longitud_contenido": len(contenido),
                "fecha_extraccion": time.strftime("%Y-%m-%d %H:%M:%S"),
                "calidad_extraccion": evaluate_extraction_quality(titulo, fecha, contenido)
            }
        }
    except Exception as e:
        return {
            "error": f"Error al analizar HTML: {str(e)}",
            "id": None,
            "titulo": "Error de parsing",
            "fecha_publicacion": "No disponible",
            "resumen": "No se pudo extraer contenido"
        }

def extract_id_from_url(url: str) -> int:
    """Extrae ID de norma desde URL"""
    if not url:
        return None
    
    # Buscar patrones de ID en la URL
    patterns = [
        r'idNorma=(\d+)',
        r'norma/(\d+)',
        r'ley/(\d+)',
        r'id=(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return int(match.group(1))
    
    return None

def generate_id_from_title(titulo: str) -> int:
    """Genera ID pseudo-único basado en el título"""
    if not titulo:
        return 999999
    
    # Hash simple del título para generar ID
    return abs(hash(titulo)) % 1000000

def evaluate_extraction_quality(titulo: str, fecha: str, contenido: str) -> str:
    """Evalúa la calidad de la extracción"""
    score = 0
    
    if titulo and titulo != "Sin título":
        score += 3
    if fecha and fecha != "Fecha no disponible":
        score += 2
    if contenido and contenido != "Contenido no disponible" and len(contenido) > 100:
        score += 5
    
    if score >= 8:
        return "Alta"
    elif score >= 5:
        return "Media"
    else:
        return "Baja"

@router.get("/buscar")
def buscar_norma(palabra: str = Query(..., min_length=3, description="Palabra clave legal a buscar en Ley Chile")):
    """Busca normas legales en BCN con análisis mejorado"""
    try:
        # Codificar término de búsqueda
        palabra_encoded = quote_plus(palabra)
        
        # URLs alternativas para búsqueda
        urls = [
            f"https://www.bcn.cl/leychile/consulta/portada_hl?tipo=0&palabra={palabra_encoded}",
            f"https://www.bcn.cl/leychile/consulta/busqueda_basica?palabra={palabra_encoded}",
            f"https://www.bcn.cl/leychile/navegar?idNorma=&buscar={palabra_encoded}"
        ]
        
        contenido_extraido = None
        url_exitosa = None
        
        # Intentar con diferentes URLs
        for url in urls:
            try:
                response = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
                if response.status_code == 200 and len(response.text) > 1000:
                    contenido_extraido = parse_html_bcn(response.text, url)
                    url_exitosa = url
                    break
                time.sleep(1)  # Pausa entre requests
            except Exception as e:
                continue
        
        if not contenido_extraido:
            return create_fallback_search_response(palabra)
        
        # Analizar relevancia del resultado
        relevancia = analyze_search_relevance(palabra, contenido_extraido)
        
        resultado = {
            "respuesta": f"Búsqueda completada para '{palabra}' en BCN. {relevancia['descripcion']}",
            "clasificacion": relevancia['nivel'],
            "justificacion": f"Resultado obtenido desde BCN con calidad {contenido_extraido.get('metadatos', {}).get('calidad_extraccion', 'No evaluada')}",
            "base_legal": {
                "BCN - Biblioteca del Congreso Nacional": "Fuente oficial de legislación chilena",
                "Norma encontrada": contenido_extraido.get('titulo', 'Sin título')
            },
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": f"Búsqueda: {palabra} → Resultado: {contenido_extraido.get('titulo', 'N/A')}",
            "sintesis_audio": f"Se encontró normativa relacionada con {palabra}",
            "fuentes": [url_exitosa] if url_exitosa else [],
            "logs": {
                "input": {
                    "palabra": palabra,
                    "palabra_encoded": palabra_encoded
                },
                "output": contenido_extraido,
                "metadatos": {
                    "url_utilizada": url_exitosa,
                    "tiempo_busqueda": time.time()
                }
            }
        }
        
        dual = output_dual(resultado)
        return JSONResponse(content={
            **dual, 
            "id": contenido_extraido.get("id")
        })
        
    except Exception as e:
        return _error_response("buscar_norma", palabra, e)

def analyze_search_relevance(palabra: str, contenido: dict) -> dict:
    """Analiza la relevancia del resultado de búsqueda"""
    titulo = contenido.get('titulo', '').lower()
    resumen = contenido.get('resumen', '').lower()
    palabra_lower = palabra.lower()
    
    # Calcular coincidencias
    coincidencias_titulo = titulo.count(palabra_lower)
    coincidencias_resumen = resumen.count(palabra_lower)
    
    total_coincidencias = coincidencias_titulo + coincidencias_resumen
    
    if total_coincidencias >= 3 or coincidencias_titulo >= 1:
        return {
            "nivel": "Fuerte",
            "descripcion": f"Alta relevancia: {total_coincidencias} coincidencias encontradas"
        }
    elif total_coincidencias >= 1:
        return {
            "nivel": "Moderada", 
            "descripcion": f"Relevancia moderada: {total_coincidencias} coincidencias encontradas"
        }
    else:
        return {
            "nivel": "Débil",
            "descripcion": "Baja relevancia: pocas coincidencias directas"
        }

def create_fallback_search_response(palabra: str) -> JSONResponse:
    """Crea respuesta de fallback cuando BCN no está disponible"""
    resultado = {
        "respuesta": f"Búsqueda simulada para '{palabra}' (BCN no disponible temporalmente)",
        "clasificacion": "Simulada",
        "justificacion": "Resultado generado localmente debido a indisponibilidad de BCN",
        "base_legal": {
            "Nota": "Este es un resultado simulado. BCN no respondió adecuadamente."
        },
        "logs": {
            "input": palabra,
            "output": "Fallback activado",
            "status": "bcn_unavailable"
        }
    }
    
    dual = output_dual(resultado)
    return JSONResponse(content={**dual, "id": 999999})

@router.get("/norma/{id_norma}")
def obtener_norma(id_norma: int):
    """Obtiene norma específica por ID con análisis detallado"""
    try:
        # URLs alternativas para obtener norma
        urls = [
            f"https://www.bcn.cl/leychile/navegar?idNorma={id_norma}",
            f"https://www.bcn.cl/leychile/consulta/norma?idNorma={id_norma}",
            f"https://www.leychile.cl/N?i={id_norma}"
        ]
        
        contenido_extraido = None
        url_exitosa = None
        
        for url in urls:
            try:
                response = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
                if response.status_code == 200:
                    contenido_extraido = parse_html_bcn(response.text, url)
                    if not contenido_extraido.get('error'):
                        url_exitosa = url
                        break
                time.sleep(1)
            except Exception:
                continue
        
        if not contenido_extraido or contenido_extraido.get('error'):
            raise HTTPException(status_code=404, detail=f"Norma {id_norma} no encontrada en BCN")
        
        resultado = {
            "respuesta": f"Norma BCN ID {id_norma} obtenida exitosamente: {contenido_extraido.get('titulo', 'Sin título')}",
            "clasificacion": "Fuerte",
            "justificacion": f"Norma extraída directamente desde BCN con calidad {contenido_extraido.get('metadatos', {}).get('calidad_extraccion', 'No evaluada')}",
            "base_legal": {
                "ID BCN": str(id_norma),
                "Título": contenido_extraido.get('titulo', 'Sin título'),
                "Fecha": contenido_extraido.get('fecha_publicacion', 'No disponible')
            },
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": f"Norma ID: {id_norma}",
            "sintesis_audio": f"Norma {id_norma} consultada en BCN",
            "fuentes": [url_exitosa] if url_exitosa else [],
            "logs": {
                "input": id_norma,
                "output": contenido_extraido,
                "url_utilizada": url_exitosa
            }
        }
        
        dual = output_dual(resultado)
        return JSONResponse(content=dual)
        
    except HTTPException:
        raise
    except Exception as e:
        return _error_response("obtener_norma", id_norma, e)

def _error_response(func: str, input_data, exception: Exception):
    """Genera respuesta de error estructurada"""
    error_msg = f"Error en {func}: {str(exception)}"
    return JSONResponse(
        status_code=500,
        content=create_error_response(error_msg, f"Input: {input_data}")
    )