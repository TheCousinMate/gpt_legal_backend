from fastapi import APIRouter

# Importar todos los routers individuales
from modules.root import router as root_router
from modules.predict import router as predict_router
from modules.reflexion import router as reflexion_router
from modules.vision_forense import router as vision_router
from modules.legislacion_bcn import router as legislacion_router
from modules.corpus_legal import router as corpus_router
from modules.prediccion_bayesiana import router as bayes_router
from modules.status import router as status_router
from modules.interprete import router as interprete_router

# Crear un router principal que agrupa todo
router_universal = APIRouter()

# Incluir todos los routers importados
router_universal.include_router(root_router)
router_universal.include_router(predict_router)
router_universal.include_router(reflexion_router)
router_universal.include_router(vision_router)
router_universal.include_router(legislacion_router)
router_universal.include_router(corpus_router)
router_universal.include_router(bayes_router)
router_universal.include_router(status_router)
router_universal.include_router(interprete_router)
