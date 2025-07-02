from dataclasses import dataclass
from PySide6.scripts.project_lib import Singleton


@dataclass
class FSAction:
    type: str
    args: list[str]


class IAIntegration(metaclass=Singleton):
    def get_audit(
        self, prompt: str, dossier: dict[str, dict]
    ) -> tuple[list[FSAction], str]:
        pass

    def get_new(self, prompt: str) -> tuple[list[FSAction], str]:
        pass
