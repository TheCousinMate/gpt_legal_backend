# generar_modelo.py
from pathlib import Path
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# entrenar algo mínimo
modelo = make_pipeline(CountVectorizer(), MultinomialNB())
modelo.fit(["placeholder"], ["General"])

# ruta final
ruta = Path("modules") / "modelo_bayesiano.joblib"
ruta.parent.mkdir(exist_ok=True)
joblib.dump(modelo, ruta)
print(f"✅ Modelo guardado en {ruta.absolute()}")
