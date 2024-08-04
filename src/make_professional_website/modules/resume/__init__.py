from pathlib import Path
from jinja2 import Template
from make_professional_website import Module, get_file_directory_path
from make_professional_website.output_file import OutputFile

MODULE_PATH = get_file_directory_path(__file__)

class Resume(Module):
    def get_output_files(self, globals, content):
        # Load up the template.
        template_path = MODULE_PATH / "template.html"
        with template_path.open("r") as f:
            template = Template(f.read(), autoescape=True)

        print(f"        [+] Loaded resume template")

        # Render the content
        rendered_website_content = template.render({
            "content": content,
            "globals": globals,
            "pdf": False,
        })

        # Render the content intended for PDF
        rendered_pdf_content = template.render({
            "content": content,
            "globals": globals,
            "pdf": True,
        })

        return [
            OutputFile(Path("resume.html"), rendered_website_content),
            # XXX: A hack automatically does not include domain prefix for this path
            OutputFile(Path("resume+pdf.html"), rendered_pdf_content),
        ]
