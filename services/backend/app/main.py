from fastapi import FastAPI

from services.backend.app.routes.views import router

app = FastAPI(title="AppAdvanture")

app.include_router(router)




