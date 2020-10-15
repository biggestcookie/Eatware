from fastapi import APIRouter, FastAPI, status
from fastapi.responses import Response

from routes import dialogflow, slack


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(dialogflow.router, prefix="/df")
    router.include_router(slack.router, prefix="/slack")
    return router


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(get_router(), prefix="/api")
    return app


app = get_app()


@app.get("/", response_class=Response)
def base() -> Response:
    return Response(status_code=status.HTTP_200_OK)
