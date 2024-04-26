from htmlmin import minify
from os import path
import glob

LANG = "ES"

TEMPLATES = [
    "aula.html",
    "aula/new.html",
    "aula/edit.html",
    "aula/NAVBAR_AULA_LOCAL.html",
    "aula/NAVBAR_AULA.html",
    "aula/-/index.html",
    "aula/-/alumnos.html",
    "aula/-/alumnos/new.html",
    "aula/-/alumnos/-.html",
    "aula/-/menu-comedor.html",
    "START-PAGE.html",
    "END-PAGE.html",
]
STATIC_FILES = [
    "static__icons__512x512.png",
    "static__icons__favicon.ico",
]


def get_template(file: str) -> str:
    with open(path.join("src/input/", file), "r") as f:
        contents = f.read()
        return minify(
            contents,
            remove_comments=True,
            reduce_boolean_attributes=True,
            remove_optional_attribute_quotes=False,
        )


def build() -> dict:
    output = {}
    for template in TEMPLATES:
        output[template] = get_template(template)
    return output


def dump(result: dict) -> None:
    with open(f"OTA/LocalAxel/{LANG}/OTA_Files/templates.yaml", "w") as f:
        f.write("TEMPLATES: " + str(result) + "\n")
        f.write("FILES: " + str(STATIC_FILES) + "\n")
    return


if __name__ == "__main__":
    dump(build())
