from yaml import safe_load
from jinja2 import Template
from pathlib import Path
import os

TEMPLATE_PATH = Path(os.path.os.path.realpath(__file__)).parent

LANDING_PAGE_TEMPLATE_NAME = "resume"

def make_professional_website():
    globals_path = Path("globals.yaml")
    try:
        with globals_path.open("r") as f:
            globals = safe_load(f)
    except:
        print("Error: Could not load globals.yaml")
        return 1
    if "Domains" not in globals:
        print("Error: globals.yaml must contain at least one domain.")
        return 1

    for g in globals:
        os.environ[g] = globals[g]

    generated_pdf_html = False
    for domain in globals["Domains"]:
        os.environ["Domain"] = domain
        globals["Domain"] = domain

        for template_path in TEMPLATE_PATH.glob("*.html")
            name = template_path.stem
            yaml_path = Path(f"{name}.yaml")
            if not yaml_path.exists():
                continue
            try:
                with yaml_path.open("r") as f:
                    yaml = safe_load(f)
            except:
                print(f"Error: Could not load {name}.yaml")
                return 1

            print(f"[+] Loaded {name}.yaml")

            try:
                with template_path.open("r") as f:
                    template = Template(f.read(), autoescape=True)
            except:
                print(f"Could not load {name}.html")
                return 1

            print(f"[+] Loaded {name}.html")

            html = template.render({
                name: yaml,
                "globals": globals,
                "pdf": False,
            })

            output_path = Path(domain) / ("index.html" if name == LANDING_PAGE_TEMPLATE_NAME else f"{name}.html")

            with output_path.open("w") as f:
                f.write(html)

            print(f"[+] Generated {output_path}")

            if (name == "resume") and ("PDF" in yaml) and (yaml["PDF"]) and (not generated_pdf_html):
                pdf_html = template.render({
                    name: yaml,
                    "globals": globals,
                    "pdf": True,
                })
                with open("pdf.html", "w") as f:
                    f.write(pdf_html)
                print("[+] Generated pdf.html")
                generated_pdf_html = True
    return 0
