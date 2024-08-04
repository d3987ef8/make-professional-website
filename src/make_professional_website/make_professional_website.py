from yaml import safe_load
from jinja2 import Template
from pathlib import Path
import sys
import os

sys.tracebacklimit = 0

TEMPLATE_PATH = Path(os.path.os.path.realpath(__file__)).parent

LANDING_PAGE_TEMPLATE_NAME = "resume"

def make_professional_website():

    # Load globals

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

    # Flag used to ensure we only generate pdf.html once

    generated_pdf_html = False

    # Main loop: For each domain

    for domain in globals["Domains"]:

        # Set "Domain" global variable and initialize sitemap paths to empty list

        globals["Domain"] = domain
        sitemap_paths = []

        # Inner loop: For each built-in template

        for template_path in TEMPLATE_PATH.glob("**/*.html"):

            if len(template_path.parts) == 1 + len(TEMPLATE_PATH.parts):
                # If the template is not in a subdirectory, extract the name from
                # the stem of the file
                name = template_path.stem

                # The place we will output the rendered content to
                output_path = f"{name}.html"

                # Remember that we will not need a subdirectory for this output
                # file.
                should_mkdir = False
            else:
                # Otherwise if it is in a subdirectory, select the name of the
                # directory as the name of the templates. This is used in cases
                # where there are multiple HTML Jinja2 template files
                # that are associated.
                name = template_path.parts[-2]

                # The place we will output the rendered content to
                output_path = f"{name}/{template_path.parts[-1]}"

                # Remember to make a subdirectory in the website raw HTML output
                should_mkdir = True

            # Find the yaml file in the current working directory that is
            # expected with this template.

            yaml_path = Path(f"{name}.yaml")
            if not yaml_path.exists():
                # If it doesn't exist, there is nothing more to do with this
                # template path.
                continue

            # Try to read the YAML file then print status to the terminal.

            try:
                with yaml_path.open("r") as f:
                    raw_txt = f.read()
                    for g in globals:
                        if isinstance(globals[g], str):
                            # Substitute in global variables, denoted by
                            # __VariableName__
                            raw_txt = raw_txt.replace(f"__{g}__", globals[g])
                    yaml = safe_load(raw_txt)
            except Exception as e:
                print(f"Error: Could not load {name}.yaml")
                print(e)
                return 1

            print(f"[+] Loaded {name}.yaml")

            # Now try to load the built-in template file, and print status.

            try:
                with template_path.open("r") as f:
                    template = Template(f.read(), autoescape=True)
            except Exception as e:
                print(f"Could not load {output_path} template")
                print(e)
                return 1

            print(f"[+] Loaded {output_path} template")

            # Now render the template with the data in the YAML file.
            # Specify "pdf": False to indicate it is intended for the web and
            # not intended for PDF rendering.

            html = template.render({
                name: yaml,
                "globals": globals,
                "pdf": False,
            })

            # Add the path of the HTML output file to the list of URLs we will
            # include in the sitemap.

            if name == LANDING_PAGE_TEMPLATE_NAME:
                sitemap_paths.append("")
            elif output_path.endswith("index.html"):
                sitemap_paths.append(f"{output_path.parent}/")
            else:
                sitemap_paths.append(output_path)

            # Update the output path to include the domain as the initial
            # subdirectory.
            output_path = Path(domain) / ("index.html" if name == LANDING_PAGE_TEMPLATE_NAME else output_path)

            # Make sure to make the subdirectory that holds all the HTML files related to this module.
            if should_mkdir:
                output_path.parent.mkdir(exist_ok=True)

            # Now actually output the rendered template
            with output_path.open("w") as f:
                f.write(html)

            # Print status message.
            print(f"[+] Generated {output_path}")

            # Check if we're going to do the hacky pdf.html thing for the
            # resume template, and if so then do the hacky thing.
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

        # For each domain, generate a sitemap.xml
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
