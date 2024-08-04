from pathlib import Path
from jinja2 import Template
from make_professional_website import Module, get_file_directory_path
from make_professional_website.output_file import OutputFile

MODULE_PATH = get_file_directory_path(__file__)

class Email(Module):
    def load_template(self, name):
        template_path = MODULE_PATH / f"{name}.html"
        with template_path.open("r") as f:
            return Template(f.read(), autoescape=True)
        print(f"        [+] Loaded {name} template for Email module")

    def get_output_files(self, globals, content):
        output_files = []
        for name in ["Form", "Sent"]:
            rendered_website_content = self.load_template(name).render({
                "content": content,
                "globals": globals,
            })
            output_files.append(
                OutputFile(
                    Path(f"email/{name}.html"),
                    rendered_website_content,
                ),
            )

        return output_files
