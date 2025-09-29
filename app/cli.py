from fire import Fire
from typing import List
from code_project_manager import CodeProjectManager, ProjectData


class CodeProjectManagerCli:

    def __init__(self, projects_json_db="projects.json"):
        self.p = CodeProjectManager(projects_json_db)

    def read(self) -> List[ProjectData]:
        return self.p.read()

    def add(self, name: str, path: str, tags: str, notes_file: str) -> ProjectData:
        old_state = self.p.__state__
        tags_list = tags.split(" ")
        res = self.p.add(name, path, tags_list, notes_file)
        self.p.commit(old_state)
        return res

    def update(
        self,
        id,
        name: str | None = None,
        path: str | None = None,
        tags: str | None = None,
        notes_file: str | None = None
    ) -> ProjectData:
        old_state = self.p.__state__
        res = self.p.update(id, name, path, tags, notes_file)
        self.p.commit(old_state)
        return res

    def delete(self, id: int, delete_notes = False) -> int:
        old_state = self.p.__state__
        res = self.p.delete(id, delete_notes)
        self.p.commit(old_state)
        return res

    def run_id(self, id: int):
        self.p.run_id(id)


if __name__ == "__main__":
    Fire(CodeProjectManagerCli)
