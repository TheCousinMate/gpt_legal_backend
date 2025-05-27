# ?? Forensic Legal Cognition 4.1

**Desarrollado por:** Kabir K. Hazbun Crovetto  
**Contacto:** khazbun@gmail.com  
**Repositorio:** [gpt_legal_backend](https://github.com/TheCousinMate/gpt_legal_backend)  
**Licencia:** Registrado en Safe Creative. Codigo privado protegido.

---

## ?? Descripcion

API chilena de analisis juridico automatizado, con capacidades avanzadas de:

- Interpretacion doctrinal
- Evaluacion forense y predictiva
- Busqueda normativa y textual
- Analisis de imagenes legales

Mas de **50 millones de palabras procesadas**, consolidando un sistema experto para litigacion, cumplimiento normativo y control de legalidad.

---

## ?? Instrucciones de uso local

### 1. Clonar repositorio
```bash
git clone https://github.com/TheCousinMate/gpt_legal_backend.git
cd gpt_legal_backend
```

### 2. Instalar entorno
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar en local
```bash
uvicorn main:app --reload
```

Accede a:  
- `http://localhost:8000/docs` ¡÷ Swagger UI  
- `http://localhost:8000/status/json` ¡÷ Estado sistema  
- `http://localhost:8000/static/openapi.yaml` ¡÷ Esquema OpenAPI

---

## ??? Seguridad

- Todos los datos son procesados en memoria.
- No se almacenan entradas del usuario.
- No se permite entrenamiento con datos externos.
- Para despliegue publico, agregar validaciones de IP y token si se requiere.

---

## ?? Licencia

Esta obra esta registrada y protegida por Safe Creative.  
Prohibida la reproduccion, redistribucion, entrenamiento IA y uso comercial sin autorizacion.  
Ver archivo `LICENSE.txt` para detalles legales.