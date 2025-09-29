from json import load, dump
import subprocess

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ProjectData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    path: Optional[str] = None
    tags: Optional[List[str]] = []

class CodeProjectManager:

    def __init__(self, projects_json_db="projects.json"):
        self.projects_json_db = projects_json_db
        self.projects: List[ProjectData] = self.read_db(self.projects_json_db)

    @property
    def __state__(self):
        return {"projects": self.projects, "projects_json_db": self.projects_json_db}

    @staticmethod
    def read_db(project_json_db):
        return load(open(project_json_db, "r"))

    @staticmethod
    def save_db(obj, project_json_db):
        dump(obj, open(project_json_db, "w"))

    def get_latest_id(self):
        return max([x["id"] for x in self.projects])

    def read(self) -> List[ProjectData]:
        return self.projects

    def add(self, name: str, path: str, tags: str) -> ProjectData:
        id = self.get_latest_id() + 1
        p = {"id": id, "name": name, "path": path, "tags": tags}
        self.projects.append(p)
        return p

    def update(
        self,
        id,
        name: str | None = None,
        path: str | None = None,
        tags: str | None = None,
    ) -> ProjectData:
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            self.projects.remove(res[0])
            p = res[0]
            if name != None:
                p["name"] = name
            if path != None:
                p["path"] = path
            if tags != None:
                p["tags"] = tags
            self.projects.append(p)
        return p

    def delete(self, id: int) -> int:
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            self.projects.remove(res[0])
        return res[0]["id"]

    def run_id(self, id: int):
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            path = res[0]["path"]
            subprocess.run(["code", path])


    def commit(self, old_state = None):
        try:
            self.save_db(self.projects, self.projects_json_db)
            return True
        except Exception as ex:
            print("Error in commit to db", f"{ex.__class__.__name__}: {str(ex)}")
            if old_state != None:
                ok = self.rollback(old_state)
                if ok:
                    print("Rolled back")
                else:
                    print("Error rolling back...")
            return False
    
    def rollback(self, state: Dict[str, Any]):
        try:
            self.save_db(state.get("projects",[]), state.get("projects_json_db", "projects.json"))
            return True
        except Exception as ex:
            print("Error in rollback of changes", f"{ex.__class__.__name__}: {str(ex)}")
            return False
