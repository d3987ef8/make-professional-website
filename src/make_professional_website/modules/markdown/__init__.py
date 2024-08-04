from pathlib import Path
from jinja2 import Template
from markdown import markdown
from make_professional_website import Module, get_file_directory_path
from make_professional_website.output_file import OutputFile

MODULE_PATH = get_file_directory_path(__file__)

class Markdown(Module):
    def get_output_files(self, globals, content):
        name = content["__name__"]

        # Load up the template.
        template_path = MODULE_PATH / "template.html"
        with template_path.open("r") as f:
            template = Template(f.read(), autoescape=False)

        print(f"        [+] Loaded {name} template")

        # Replace content markdown with rendered markdown content
        content["Markdown"] = markdown(content["Markdown"])

        # Render the content
        rendered_content = template.render({
            "content": content,
            "globals": globals,
        })

        return [
            OutputFile(Path(f"{content['__name__']}.html"), rendered_content),
        ]
