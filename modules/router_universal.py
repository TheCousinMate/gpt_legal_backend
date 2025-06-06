# modules/router_universal.py
from fastapi import APIRouter
from modules.root import router as root_router
from modules.reflexion import router as reflexion_router
from modules.predict import router as predict_router
from modules.vision_forense import router as vision_router
from modules.forensics_proxy import router as forensics_router
from modules.bcn_parser import router as bcn_parser_router
from modules.bcn_text_search_parser import router as text_search_router

router = APIRouter()
router.include_router(root_router)
router.include_router(reflexion_router)
router.include_router(predict_router)
router.include_router(vision_router)
router.include_router(forensics_router)
router.include_router(bcn_parser_router)
router.include_router(text_search_router)
