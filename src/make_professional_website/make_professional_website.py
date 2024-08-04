from yaml import safe_load
from jinja2 import Template
from pathlib import Path
import sys
import os

sys.tracebacklimit = 0

TEMPLATE_PATH = Path(os.path.os.path.realpath(__file__)).parent

LANDING_PAGE_TEMPLATE_NAME = "resume"

def make_professional_website():
    globals_path = Path("globals.yaml")
    try:
        with globals_path.open("r") as f:
            globals = safe_load(f)
    except Exception as e:
        print("Error: Could not load globals.yaml")
        print(e)
        return 1
    if "Domains" not in globals:
        print("Error: globals.yaml must contain at least one domain.")
        return 1

    generated_pdf_html = False
    for domain in globals["Domains"]:
        globals["Domain"] = domain
        sitemap_paths = []

        for template_path in TEMPLATE_PATH.glob("**/*.html"):
            if len(template_path.parts) == 1 + len(TEMPLATE_PATH.parts):
                name = template_path.stem
                output_path = f"{name}.html"
                should_mkdir = False
            else:
                name = template_path.parts[-2]
                output_path = f"{name}/{template_path.parts[-1]}"
                should_mkdir = True
            yaml_path = Path(f"{name}.yaml")
            if not yaml_path.exists():
                continue
            try:
                with yaml_path.open("r") as f:
                    raw_txt = f.read()
                    for g in globals:
                        if isinstance(globals[g], str):
                            raw_txt = raw_txt.replace(f"__{g}__", globals[g])
                    yaml = safe_load(raw_txt)
            except Exception as e:
                print(f"Error: Could not load {name}.yaml")
                print(e)
                return 1

            print(f"[+] Loaded {name}.yaml")

            try:
                with template_path.open("r") as f:
                    template = Template(f.read(), autoescape=True)
            except Exception as e:
                print(f"Could not load {output_path} template")
                print(e)
                return 1

            print(f"[+] Loaded {output_path} template")

            html = template.render({
                name: yaml,
                "globals": globals,
                "pdf": False,
            })

            if name == LANDING_PAGE_TEMPLATE_NAME:
                sitemap_paths.append("")
            elif output_path.endswith("index.html"):
                sitemap_paths.append(f"{output_path.parent}/")
            else:
                sitemap_paths.append(output_path)

            output_path = Path(domain) / ("index.html" if name == LANDING_PAGE_TEMPLATE_NAME else output_path)

            if should_mkdir:
                output_path.parent.mkdir(exist_ok=True)

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
        try:
            with Path(TEMPLATE_PATH / "sitemap.xml").open("r") as f:
                template = Template(f.read(), autoescape=True)
        except Exception as e:
            print("Could not load sitemap.xml template")
            print(e)
            return 1
        sitemap_xml = template.render({
            "paths": sitemap_paths,
            "globals": globals,
        })
        with (Path(domain) / "sitemap.xml").open("w") as f:
            f.write(sitemap_xml)
    return 0
