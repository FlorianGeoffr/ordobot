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


# noinspection PyTypeChecker
class IAIntegration(metaclass=Singleton):
    def __init__(self):
        if not Config().get("chatgpt_api_key", None):
            raise ValueError(
                "API key for ChatGPT is not set. Please configure it in the settings."
            )
        self.client = OpenAI(api_key=Config().get("chatgpt_api_key", None))
        self.model = Config().get("ai_model", "gpt-4.1")  # Default model

    def get_audit(
        self, prompt: str, dossier: dict[str, dict]
    ) -> tuple[list[FSAction], str]:
        string_dossier = self.generate_str_dossier(dossier)
        print(f"Current structure:\n{string_dossier}")
        response = self.client.chat.completions.create(
            model=self.model,  # Use dynamic model
            messages=[
                {
                    "role": "system",
                    "content": f"""
You analyze and improve a folder structure.

Output: ONE LINE. Format: mk:path;rm:path;mv:src:dest;mvc:src:dest;me:summary in French

Rules:
- Only folders (no files)
- All paths are folder names
- mv: must follow mv:source:destination (exactly two `:`)
- Each mv: moves one folder only
- Specify the full path for the mk, rm, and mv commands.
- Use `;` as separator (no spaces)
- No duplicates, accents, smart quotes, long dashes, or incomplete commands
- Allowed chars: letters, numbers, / . ' - , and space
- Do not delete anything unless explicitly instructed
- me: must be last and written in French
- mvc: is for moving contents of a folder, format: mvc:source:destination

create the new structure with mk
then mvc the content of old folders to new ones
and finally rm the old folders

Current structure:
{string_dossier}
""",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return parse_output(response.choices[0].message.content)

    def get_new(self, prompt: str) -> tuple[list[FSAction], str]:
        response = self.client.chat.completions.create(
            model=self.model,  # Use dynamic model
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
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append(f"{'  ' * (len(path.split('/')) - 1)} {key}/")
                    traverse(value, f"{path}/{key}")
                else :
                    lines.append(
                        f"{'  ' * (len(path.split('/')) - 1)} {key}"
                    )

        traverse(dossier)
        return "\n".join(lines)
