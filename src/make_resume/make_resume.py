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

    print("- Loaded resume.yaml")

    with TEMPLATE_PATH.open() as f:
        template = Template(f.read(), autoescape=True)

    print("- Loaded template.html from make-resume package")

    for domain in resume["Domains"]:
        email = f"contact@{domain}"
        portfolio = "https://www.{domain}"

        html = template.render({
          "resume": resume,
          "pdf": False,
          "email": email,
          "portfolio": portfolio,
        })

        with open(f"{domain}/index.html", "w") as f:
            f.write(html)

        print(f"- Generated {domain}/index.html")

    domain = resume["Domains"][0]
    email = f"contact@{domain}"
    portfolio = "https://www.{domain}"

    pdf = template.render({
      "resume": resume,
      "pdf": True,
      "email": email,
      "portfolio": portfolio,
    })

    with open("pdf.html", "w") as f:
        f.write(pdf)

    print("- Generated pdf.html")

    return 0
