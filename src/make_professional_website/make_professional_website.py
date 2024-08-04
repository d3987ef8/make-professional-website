from yaml import safe_load
from pathlib import Path
from .__init__ import get_file_directory_path
import sys

# Modules
from make_professional_website.modules.resume import Resume
from make_professional_website.modules.email import Email
from make_professional_website.modules.sitemap import Sitemap
from make_professional_website.modules.markdown import Markdown

MODULES = {
    "resume": Resume(),
    "email": Email(),
    "sitemap": Sitemap(),
    "markdown": Markdown(),
}

sys.tracebacklimit = 0

LANDING_PAGE_MODULE_NAME = "resume"

SITEMAP_TEMPLATE_PATH = get_file_directory_path(__file__) / "sitemap.xml"

def make_professional_website():
    # Load globals
    globals_path = Path("content/globals.yaml")
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

    # Main loop: For each domain
    for domain in globals["Domains"]:

        # Status update
        print(f"[+] Processing {domain}")

        # Set "Domain" global variable and initialize sitemap paths to empty list
        globals["Domain"] = domain
        sitemap_paths = []

        # Inner loop: For each YAML file in the current directory.
        for yaml_path in Path("content").glob("*.yaml"):
            # Special-case globals.yaml since we already handled that above.
            if yaml_path.parts[-1] == "globals.yaml":
                continue

            name = yaml_path.stem

            # Try to read the YAML file then print status to the terminal.
            try:
                with yaml_path.open("r") as f:
                    raw_txt = f.read()
                    for g in globals:
                        if isinstance(globals[g], str):
                            # Substitute in global variables, denoted by
                            # __VariableName__
                            raw_txt = raw_txt.replace(f"__{g}__", globals[g])
                    content = safe_load(raw_txt)
            except Exception as e:
                print(f"Error: Could not load {name}.yaml")
                print(e)
                return 1
            print(f"    [+] Loaded {name}.yaml")

            content["__name__"] = name

            # Find the module name and path
            if "Module" in content:
                module_name = content["Module"]
            else:
                module_name = yaml_path.stem

            # Ensure the module exists
            if not module_name in MODULES:
                print(f"Error: Module does not exist: {module_name}")
                return 1

            # Get path and content for output file and write to disk
            for output_file in MODULES[module_name].get_output_files(globals, content):
                output_file.path.parent.mkdir(exist_ok=True)
                domain_specific_path = Path(domain) / output_file.path

                with domain_specific_path.open("w") as f:
                    f.write(output_file.rendered_content)
                print(f"        [+] Generated {domain_specific_path}")

                # Remember the output path for when we generate the sitemap.xml
                if output_file.path.parts[-1] == "pdf.html":
                    pass
                elif output_file.path.parts[-1] == "index.html":
                    if len(output_file.path.parts) == 1:
                        sitemap_paths.append("")
                    else:
                        sitemap_paths.append(str(output_file.path).replace("index.html", ""))
                else:
                    sitemap_paths.append(str(output_file.path))

        content = {"paths": sitemap_paths}
        [output_file] = MODULES["sitemap"].get_output_files(globals, content)
        domain_specific_path = Path(domain) / output_file.path
        with domain_specific_path.open("w") as f:
            f.write(output_file.rendered_content)
        print(f"    [+] Generated {domain_specific_path}")
    return 0
