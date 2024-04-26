from microdot import Microdot
from pysondb import db
from datetime import datetime
from utils import requests
import yaml

config = yaml.safe_load(open("config.yaml"))
templates = yaml.safe_load(open("OTA_Files/templates.yaml"))

db_alumnos = db.getDb("db.alumnos.json")
db_aulas = db.getDb("db.aulas.json")

app = Microdot()

FOLDER_NAME = "OTA_Files"

menu = {}


def read(file: str):
    return templates["TEMPLATES"][file]


def redirect(path: str):
    return "", 301, {"Location": path}


def reload_comedor():
    if config["Menu_Disable"]:
        return
    global menu
    menu = requests.get(config["Menu_URL"]).json()


@app.get("/static/<file>")
async def static(req, file: str):
    f = file.split("__")
    with open(f"{FOLDER_NAME}/static__" + "__".join(f), "rb") as f:
        return f.read()


def build_page(template_file: list, modo: str = "default", **kwargs):
    template = read(template_file).split("~")
    output = []
    if modo == "edit_alumno":
        edit_alumno = db_alumnos.getById(int(kwargs["alumno_id"]))
    else:
        edit_alumno = {
            "nombre": "",
            "correo": "",
            "telefono": "",
            "extra": "",
            "aula": "",
        }
    if modo == "edit_aula":
        edit_aula = db_aulas.getByQuery({"codigo": kwargs["aula"]})[0]
    for value in template:
        if value == "START_PAGE":
            output.append(read("START-PAGE.html"))
            continue
        elif value == "END_PAGE":
            output.append(read("END-PAGE.html"))
        elif value == "NAVBAR_AULA_LOCAL":
            output.append(
                "".join(build_page("aula/NAVBAR_AULA_LOCAL.html", aula=kwargs["aula"]))
            )
            continue
        elif value == "NAVBAR_AULA":
            output.append("".join(build_page("aula/NAVBAR_AULA.html")))
            continue
        elif value == "LISTA_ALUMNOS":
            alumnos = db_alumnos.getByQuery({"aula": kwargs["aula"].lower()})
            alumnos_output = [
                f'<tr><th scope="row"><a href="alumnos/{alumno["id"]}">{alumno["nombre"]}</a></th><td>{alumno["correo"]}</td><td>{alumno["telefono"]}</td><td><a class="btn btn-primary" href="mailto:{alumno["correo"]}">Enviar Correo</a> <a class="btn btn-danger" href="alumnos/{alumno["id"]}/delete">Borrar</a></td></tr>'
                for alumno in alumnos
            ]
            output += alumnos_output
            continue
        elif value == "LISTA_AULAS":
            aulas = db_aulas.getAll()
            alumnos_output = [
                f'<tr><th scope="row"><a href="aula/{aula["codigo"]}">{aula["nombre"]}</a></th><td><a class="btn btn-danger" href="aula/{aula["id"]}/delete">Borrar</a></td></tr>'
                for aula in aulas
            ]
            output += alumnos_output
            continue
        elif value == "ALUMNO_NOMBRE":
            output.append(edit_alumno["nombre"])
            continue
        elif value == "ALUMNO_CORREO":
            output.append(edit_alumno["correo"])
            continue
        elif value == "ALUMNO_TELEFONO":
            output.append(edit_alumno["telefono"])
            continue
        elif value == "ALUMNO_EXTRA":
            output.append(edit_alumno["extra"])
            continue
        elif value == "AULA_NOMBRE":
            output.append(edit_aula["nombre"])
            continue
        elif value == "AULA_EXTRA":
            output.append(edit_aula["extra"])
            continue
        elif value == "CODIGO_AULA":
            output.append(kwargs["aula"])
            continue
        elif value == "MENU_COMEDOR_HOY":
            output.append(str(kwargs["hoy"]).replace("\n", "<br>"))
            continue
        elif value == "MENU_COMEDOR_TABLA":
            menu_output = [
                f'<tr><th scope="row">{dia["dia"]}</th><td>{dia["menu"]}</td></tr>'
                for dia in kwargs["menu"]
            ]
            output += menu_output
        else:
            output.append(value)
            continue
    return output


@app.get("/aula/<aula>")
async def aula__index(req, aula: str):
    aula = aula.lower()
    if aula == "new":
        return "".join(build_page("aula/new.html", aula=aula)), {
            "Content-Type": "text/html"
        }
    elif "_edit" in aula:
        eaula=aula.replace("_edit", "")
        return "".join(build_page("aula/edit.html", modo="edit_aula", aula=eaula)), {
            "Content-Type": "text/html"
        }

    return "".join(build_page("aula/-/index.html", aula=aula)), {
        "Content-Type": "text/html"
    }


@app.get("/aula")
async def aula__index(req):
    return "".join(build_page("aula.html")), {"Content-Type": "text/html"}


@app.get("/aula/<aula>/alumnos")
async def aula__alumnos__all(req, aula: str):
    aula = aula.lower()
    return "".join(build_page("aula/-/alumnos.html", aula=aula)), {
        "Content-Type": "text/html"
    }


@app.get("/aula/<aula>/alumnos/<id>")
async def aula__alumnos__get(req, aula: str, id):
    aula = aula.lower()
    if id == "new":
        return "".join(
            build_page("aula/-/alumnos/new.html", aula=aula, alumno_id=id)
        ), {"Content-Type": "text/html"}
    return "".join(
        build_page("aula/-/alumnos/-.html", modo="edit_alumno", aula=aula, alumno_id=id)
    ), {"Content-Type": "text/html"}


@app.get("/aula/<aula>/alumnos/<id>/delete")
async def aula__alumnos__delete(req, aula: str, id):
    aula = aula.lower()
    db_alumnos.deleteById(int(id))
    return redirect(f"/aula/{aula}/alumnos")


@app.get("/aula/<aula>/menu-comedor")
async def aula__menu_comedor(req, aula: str):
    aula = aula.lower()
    hoy_iso = datetime.today().isoformat().split("T")[0]
    m = [{"dia": dia, "menu": menu[dia]} for dia in menu.keys()]
    return "".join(
        build_page(
            "aula/-/menu-comedor.html",
            aula=aula,
            menu=m,
            hoy=menu.get(hoy_iso, "Hoy no hay comedor, o no se ha descargado el menu."),
        )
    ), {"Content-Type": "text/html"}


@app.post("/aula/<aula>/alumnos/<id>")
async def aula__alumnos__post(req, aula: str, id):
    aula = aula.lower()
    if id == "new":
        db_alumnos.add(
            {
                "nombre": req.form["nombre"] or "No Definido",
                "correo": req.form["correo"] or "No Definido",
                "telefono": req.form["telefono"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
                "aula": aula,
            }
        )
    else:
        db_alumnos.updateById(
            int(id),
            {
                "nombre": req.form["nombre"] or "No Definido",
                "correo": req.form["correo"] or "No Definido",
                "telefono": req.form["telefono"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
                "aula": aula,
            },
        )

    return redirect(f"/aula/{aula}/alumnos")


@app.post("/aula/<aula>")
async def aula__post(req, aula: str):
    aula = aula.lower()
    if aula == "new":
        if db_aulas.getByQuery({"codigo": req.form["codigo"]}) != []:
            return redirect(f"/_error/aula_code_used")
        db_aulas.add(
            {
                "codigo": req.form["codigo"],
                "nombre": req.form["nombre"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
            }
        )
        return redirect(f"/aula/{req.form["codigo"]}")
    else:
        db_alumnos.updateByQuery(
            {"codigo": aula},
            {
                "nombre": req.form["nombre"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
            },
        )

    return redirect(f"/aula")


@app.get("/admin/recargar_menu")
async def admin__recargar_menu(req):
    reload_comedor()
    return "Comedor Recargado."


if __name__ == "__main__":
    reload_comedor()
    app.run(host="0.0.0.0", port=17170, debug=False)
