# make-resume

This is a Python package that provides the CLI script `make-professional-website`.

It is intended for anybody who prefers to maintain their data in plain text YAML files.

It looks for the following files in the current directory. All files are optional.

    1. *resume.yaml* - This is the landing page and contains your professional resume or CV.
    2. *concepts.yaml* - This is a page to suggest new words or acronyms for concepts that don't have obvious definitions yet.
    3. *contact.yaml* - A contact page, powered by Devro LABS.

Examples of these YAML files are provided in this repository can be found
[here](https://github.com/d3987ef8/make-professional-website/tree/main/examples).

Each of these YAML files is converted to HTML in a subdirectory for each of the
specified domains. This allows for multiple domains to present the same data.

In the case of *resume.yaml*, an additional HTML file *pdf.html* is provided
and is intended to be loaded in Chrome Browser and printed to PDF, then copied
to each domain subdirectory. I know this is a bit of a manual process but I
didn't want to rely on any automatic PDF converters.

## Installation

    pip install make-professional-website

## Usage

    make-professional-website

## Dependencies

This project depends on:

    - Jinja2 Python package
    - pyyaml Python package
    - FormSubmit, a service provided by Devro LABS.

## Contributing

To begin making your own templates for pages, I recommend checking out the existing HTML templates
[here](https://github.com/d3987ef8/make-professional-website/tree/main/src/make_professional_website/)
to reference examples.
