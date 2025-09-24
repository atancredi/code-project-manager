from json import load, dump
from fire import Fire

import subprocess


class CodeProjectManager:

    def __init__(self, projects_json_db="projects.json"):
        self.project_json_db = projects_json_db
        self.projects = self.read_db(self.project_json_db)

    @staticmethod
    def read_db(project_json_db):
        return load(open(project_json_db, "r"))

    @staticmethod
    def save_db(obj, project_json_db):
        dump(obj, open(project_json_db, "w"))

    def get_latest_id(self):
        return max([x["id"] for x in self.projects])

    def read(self):
        return self.projects

    def add(self, name, path, tags):
        id = self.get_latest_id() + 1
        p = {"id": id, "name": name, "path": path, "tags": tags}
        self.projects.append(p)
        self.save_db(self.projects, self.project_json_db)
        return p

    def update(self, id, name, path, tags):
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            self.projects.remove(res[0])
            p = res[0]
            p["name"] = name
            p["path"] = path
            p["tags"] = tags
            self.projects.append(p)
        return p

    def delete(self):
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            self.projects.remove(res[0])

    def run_id(self, id):
        res = [x for x in self.projects if x["id"] == id]
        if len(res) == 0:
            raise ValueError(f"Project with ID {id} not found.")
        else:
            path = res[0]["path"]
            subprocess.run(["code", path])


if __name__ == "__main__":
    Fire(CodeProjectManager)
