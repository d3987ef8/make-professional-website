# make-professional-website (mpw)

This is a Python package that provides the CLI script `pwm` ("Professional Website Maker").

It is intended for anybody who prefers to maintain their data in plain text YAML files.

## Why make-professional-website?

  1. *Ease of Use for Beginners*: The simplicity of using YAML over HTML for beginners is a significant advantage. Many people find HTML daunting initially, so this package offers a simpler alternative. There is a focus on ease of use, especially for those new to coding or those who need to create simple websites quickly.
  2. *Niche Market*: There seems to be a niche market for this kind of tool. Beginners who want to create professional-looking websites without diving deep into HTML and CSS, as well as those who prefer a more old-school approach to web development, could find this framework very useful.
  3. *Unique Approach*: This tool's focus on minimal dependencies and code security, combined with the classical approach to frontend work, differentiates it from many modern frameworks. This could appeal to developers who are cautious about the complexity associated with many modern frontend technologies.
  4. Potential Users:
    - Hobbyists and DIYers: Individuals who want to create personal websites or projects.
    - Small Business Owners: People who need a simple, professional web presence without the overhead of learning complex web technologies.
    - Educators and Students: Educational institutions might find this tool useful for teaching the basics of web development without overwhelming students.

## How can I get started?

It looks for the following files in the current directory. All files are optional.

    1. *resume.yaml* - This is the landing page and contains your professional resume or CV.
    2. *concepts.yaml* - This is a page to suggest new words or acronyms for concepts that don't have obvious definitions yet.
    3. *contact.yaml* - A contact form.

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
