import time
import datetime as dt
import fastapi as _fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.endpoints import UserEndpoint, PostEndpoint, ContactEndpoint, AuthEndpoint
import src.database as _database
import src.config.config_trace as _tracer


def create_app() -> _fastapi.FastAPI:

    # _database.init_db.create_database()
    _tracer.config_trace_init()

    app = _fastapi.FastAPI(title='CMS FastAPI BD', description="""ChimichangApp API helps you do awesome stuff """, version="0.0.1", openapi_url="/api/v1/openapi.json")

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.mount("/static", _fastapi.staticfiles.StaticFiles(directory="src/static"), name="static")
    templates = Jinja2Templates(directory="src/templates")

    app.include_router(AuthEndpoint.router)
    app.include_router(UserEndpoint.router)
    app.include_router(PostEndpoint.router)
    app.include_router(ContactEndpoint.router)

    @app.get("/", response_class=_fastapi.responses.HTMLResponse, status_code=200)
    async def root(request: _fastapi.Request):
        return templates.TemplateResponse("index.html", {"request": request, "nome": "Chris MarSil"})  # return {"status": "OK"}

    @app.on_event("startup")
    async def startup():
        pass  # await _database.session.database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        pass  # await _database.session.database.disconnect()

    @app.middleware("http")
    async def add_process_time_header(request: _fastapi.Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["Z-Process-Time"] = str(dt.timedelta(seconds=process_time))
        return response

    @app.exception_handler(Exception)
    def validation_exception_handler(request, err):
        return _fastapi.responses.JSONResponse(status_code=400, content={"message": f"Failed to execute: {request.method}: {request.url}. Detail: {err}"})

    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    FastAPIInstrumentor.instrument_app(app, tracer_provider=_tracer.provider)

    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    SQLAlchemyInstrumentor().instrument(engine=_database.session.engine)
    SQLAlchemyInstrumentor().instrument(engine=_database.session.engine_async)

    # from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware
    # app.add_middleware(PyInstrumentProfilerMiddleware)

    return app