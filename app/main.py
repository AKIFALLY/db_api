"""
AGVC 系統 FastAPI 主程式
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json

from app.core.config import settings
from app.api.v1 import agv, eqp_port

# 建立 FastAPI 應用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AGV 車輛管理系統 API",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)


# 自定義驗證錯誤處理器（顯示詳細錯誤）
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """顯示詳細的驗證錯誤訊息"""
    print("=" * 70)
    print("[VALIDATION ERROR] 422 Unprocessable Entity")
    for error in exc.errors():
        print(f"  - Location: {error.get('loc')}")
        print(f"    Type: {error.get('type')}")
        print(f"    Message: {error.get('msg')}")
    print("=" * 70)
    from fastapi.encoders import jsonable_encoder
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()})
    )

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 請求日誌中間件（用於除錯）- 需要時可啟用
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     """記錄所有 POST/PUT/PATCH 請求的 body"""
#     if request.method in ["POST", "PUT", "PATCH"]:
#         body = await request.body()
#         print("=" * 70)
#         print(f"[{request.method}] {request.url.path}")
#         print(json.dumps(json.loads(body.decode('utf-8')), indent=2, ensure_ascii=False))
#         print("=" * 70)
#         async def receive():
#             return {"type": "http.request", "body": body, "more_body": False}
#         request = Request(request.scope, receive)
#     response = await call_next(request)
#     return response


# 根路由
@app.get("/", tags=["Root"])
def root():
    """
    根路由 - API 資訊
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# 健康檢查
@app.get("/health", tags=["Health"])
def health_check():
    """
    健康檢查端點
    """
    return {"status": "healthy"}


# 註冊 API 路由
app.include_router(
    agv.router,
    prefix=f"{settings.API_V1_PREFIX}/agv",
    tags=["AGV"]
)

app.include_router(
    eqp_port.router,
    prefix=f"{settings.API_V1_PREFIX}/eqp_port",
    tags=["EqpPort"]
)


# 啟動事件
@app.on_event("startup")
async def startup_event():
    """
    應用啟動時執行
    """
    print(f"[啟動] {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"[文檔] API Docs: http://localhost:8000/docs")
    print(f"[文檔] ReDoc: http://localhost:8000/redoc")


# 關閉事件
@app.on_event("shutdown")
async def shutdown_event():
    """
    應用關閉時執行
    """
    print(f"[關閉] {settings.PROJECT_NAME}")
