from dataclasses import dataclass
from PySide6.scripts.project_lib import Singleton
from openai import OpenAI

from assets.config import Config


@dataclass
class FSAction:
    type: str
    args: list[str]


def parse_output(output: str) -> tuple[list[FSAction], str]:
    """
    Parse the output from the AI model to extract actions and a summary.
    :param output: The output string from the AI model.
    :return: A tuple containing a list of FSAction and a summary string.
    """
    actions = []
    summary = ""

    # Example parsing logic (to be implemented based on actual output format)
    lines = output.split(";")
    for line in lines:
        if not line.startswith("me:"):
            part = line.strip().split(":")
            action = part[0].strip()
            args = part[1:]
            if action:
                actions.append(
                    FSAction(
                        type=action, args=[arg.strip() for arg in args if arg.strip()]
                    )
                )
        else:
            summary = line.replace("me:", "").strip()
    return actions, summary


class IAIntegration(metaclass=Singleton):
    def __init__(self):
        if not Config().get("chatgpt_api_key", None):
            raise ValueError(
                "API key for ChatGPT is not set. Please configure it in the settings."
            )
        self.client = OpenAI(api_key=Config().get("chatgpt_api_key", None))

    def get_audit(
        self, prompt: str, dossier: dict[str, dict]
    ) -> tuple[list[FSAction], str]:
        string_dossier = self.generate_str_dossier(dossier)
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze and improve a folder structure.\n\n"
                        "Output: ONE LINE. Format: mk:path;rm:path;mv:src:dest;me:summary in French\n\n"
                        "Rules:\n"
                        "- find good folder structure\n"
                        "- Only work with folders (no files)\n"
                        "- mk: create folder\n"
                        "- rm: remove folder\n"
                        "- mv: move/rename folder (format: mv:source:destination)\n"
                        "- specify the full path for mk:, rm:, and mv:\n"
                        "- Each mv: must contain exactly two `:` → format: mv:src/:dest/\n"
                        "- Do not shorten or omit any part of the command\n"
                        "- Each mv: must handle ONE folder only\n"
                        "- Use `;` as separator (no spaces)\n"
                        "- No duplicates, accents, smart quotes, long dashes, or incomplete commands\n"
                        "- Allowed chars: letters, numbers, / . ' - , and space\n"
                        "- Do not delete anything unless explicitly required by user instruction\n"
                        "- me: must be written in French\n\n"
                        f"Current structure:\n{string_dossier}"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def get_new(self, prompt: str) -> tuple[list[FSAction], str]:
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You generate a folder structure (no files).

Output: ONE LINE. Format: mk:folder/;mk:folder/;me:summary in French

Rules:
- Only use mk: to create folders (must end with `/`)
- Use `;` as separator (no spaces)
- No files, no duplicates, no accents, smart quotes, long dashes, or incomplete commands
- Allowed chars: letters, numbers, / . ' - , and space
- me: must be last and in French""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def generate_str_dossier(self, dossier: dict[str, dict]) -> str:
        """
        Convert the dossier dictionary into a string representation.
        l=N chemin[/si dossier]
        :param dossier: Dictionary representing the file system structure.
        {"test": {"fichier.txt": None, "dossier": {"fichier2.txt": None}}}
        """
        lines = []

        def get_number_of_lines(d):
            return sum(1 for key, value in d.items() if value is None)

        def get_extension(dict):
            list_extension = []
            for key, value in dict.items():
                if value is None:
                    list_extension.append(key.split(".")[-1])

            list_extension_unique = set(list_extension)
            return ",".join(list_extension_unique)

        def as_file(d):
            return any(value is None for value in d.values())

        def traverse(d, path=""):
            if as_file(d):
                lines.append(
                    f"{'  ' * (len(path.split('/')) - 1)} [{get_number_of_lines(d)}: {get_extension(d)}]"
                )
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append(f"{'  ' * (len(path.split('/')) - 1)} {key}/")
                    traverse(value, f"{path}/{key}")

        traverse(dossier)
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    ia_integration = IAIntegration()
    out = """mk:Projects;mv:ESTIAM E1:Projects/ESTIAM E1;mv:ESTIAM E1 copy:Projects/ESTIAM E1 copy;mv:WebstormProjects:Projects/WebstormProjects;mv:SiteInternetSquash:Projects/SiteInternetSquash;mv:saveSatisServer:Projects/saveSatisServer;mv:TOMAS_Alexandre:Projects/TOMAS_Alexandre;mv:TOMAS_Alexandre-1FCTDES-PT1:Projects/TOMAS_Alexandre-1FCTDES-PT1;mv:TOMAS_Alexandre-1FCTDES-PT2:Projects/TOMAS_Alexandre-1FCTDES-PT2;mv:STAGE:Projects/STAGE;mv:Photos iCloud de Alexandre  Tomas:Projects/Photos   iCloud de Alexandre  Tomas;mv:image:Assets;mk:Assets Project;mv:Assets Project HTML:Assets Project/HTML;mv:HackLGBT:Assets/HackLGBT;mv:testboreal:Projects/testboreal;mv:image/TOMAS_Alexandre/Assets:Assets/TOMAS_Alexandre;me:Proposition d'organisation avec un dossier principal 'Projects' pour les projets et 'Assets' pour les ressources, facilitant la navigation et la gestion."""
    actions, summary = ia_integration._IAIntegration__parse_output(out)
    print("Actions:")
    for action in actions:
        print(f"Type: {action.type}, Args: {action.args}")
    print("Summary:", summary)
    print("Actions:")
    for action in actions:
        print(f"Type: {action.type}, Args: {action.args}")
    print("Summary:", summary)
