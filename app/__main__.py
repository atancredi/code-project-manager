from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from code_project_manager import CodeProjectManager, ProjectData


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Define app
app = FastAPI(
    title="",
    version=1.1,
    description="",
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)


# Health
@app.get("/health")
async def health():
    return {"message": app.title + " " + str(app.version) + " Alive"}


ws = uvicorn.Server(
    config=uvicorn.Config(
        app=app,
        port=8080,
        host="0.0.0.0",
        log_level="info",
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
        },
    )
)


# projects
p = CodeProjectManager()


@app.get("/projects")
async def get_projects():
    return p.read()


@app.post("/projects")
async def add_projects(projects: List[ProjectData]):

    affected_ids = []
    failed = []
    for i, project in enumerate(projects):

        if project.name == None:
            failed.append((i, "missing name"))
            continue

        if project.path == None:
            failed.append((i, "missing path"))
            continue
        try:
            res = p.add(project.name, project.path, " ".join(project.tags))
            affected_ids.append(res["id"])
        except Exception as ex:
            failed.append((i, f"{ex.__class__.__name__}: {str(ex)}"))

    return JSONResponse({"success": affected_ids, "fail": failed})


@app.patch("/projects")
async def update_projects(projects: List[ProjectData]):

    updated_projects = []
    failed = []
    for i, project in enumerate(projects):
        if project.id == None:
            failed.append((project.id, "missing id"))
            continue
        try:
            res = p.update(project.id, project.name, project.path, project.tags)
            updated_projects.append(res)
        except Exception as ex:
            failed.append((i, f"{ex.__class__.__name__}: {str(ex)}"))
    return JSONResponse({"success": updated_projects, "fail": failed})


@app.delete("/projects")
async def delete_projects(project_ids: List[int]):
    affected_ids = []
    failed = []
    for id in project_ids:
        try:
            affected_id = p.delete(id)
            affected_ids.append(affected_id)
        except Exception as ex:
            failed.append((id, f"{ex.__class__.__name__}: {str(ex)}"))
    return JSONResponse({"success": affected_ids, "fail": failed})


if __name__ == "__main__":
    print("Ready to start")
    ws.run()
