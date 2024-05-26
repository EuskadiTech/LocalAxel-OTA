from htmlmin import minify
from os import path
import glob
from yaml import safe_dump

LANG = "ES"

TEMPLATES = [
    "aula.html",
    "aula/new.html",
    "aula/edit.html",
    "aula/NAVBAR_AULA_LOCAL.html",
    "aula/NAVBAR_AULA.html",
    "aula/-/index.html",
    "aula/-/soporte-tecnico.html",
    "aula/-/alumnos.html",
    "aula/-/alumnos/new.html",
    "aula/-/alumnos/-.html",
    "aula/-/menu-comedor.html",
    "aula/-/tareas.html",
    "aula/-/tareas/-.html",
    "aula/-/tareas/new.html",
    "_error/incorrect_admin_pin.html",
    "_error/aula_code_used.html",
    "smart/NAVBAR_SMART.html",
    "smart/index.html",
    "smart/new.html",
    "smart/new/aviso.html",
    "NAVBAR_ADMIN.html",
    "index.html",
    "admin.html",
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
        k = {"TEMPLATES": result, "FILES": STATIC_FILES}
        safe_dump(k, f)
    return


if __name__ == "__main__":
    dump(build())
