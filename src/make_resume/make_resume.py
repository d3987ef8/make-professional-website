from yaml import safe_load
from jinja2 import Template
from pathlib import Path
import os

TEMPLATE_PATH = Path(os.path.os.path.realpath(__file__)).parent / "template.html"

def make_resume():
    try:
        with open("resume.yaml", "r") as f:
            resume = safe_load(f)
    except:
        print("Could not load resume from resume.yaml")
        return 1

    with TEMPLATE_PATH.open() as f:
        template = Template(f.read(), autoescape=True)

    html = template.render({"resume": resume, "pdf": False})
    pdf = template.render({"resume": resume, "pdf": True})

    with open("index.html", "w") as f:
        f.write(html)

    with open("pdf.html", "w") as f:
        f.write(pdf)

    print("Generated index.html and pdf.html from resume.yaml")

    return 0
