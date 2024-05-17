from microdot import Microdot
from pysondb import db
from datetime import datetime
from utils import requests, ota_updater
import yaml

config: dict = yaml.safe_load(open("config.yaml"))
templates = yaml.safe_load(open("OTA_Files/templates.yaml"))

db_alumnos = db.getDb("db.alumnos.json")
db_aulas = db.getDb("db.aulas.json")
db_autotareas = db.getDb("db.autotareas.json")

app = Microdot()

FOLDER_NAME = "OTA_Files"
HEADERS = {"Content-Type": "text/html; charset=utf-8"}
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
    if modo == "edit_tarea":
        edit_tarea = db_autotareas.getById(int(kwargs["tarea_id"]))
    else:
        edit_tarea = {
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
        elif value == "NAVBAR_ADMIN":
            output.append("".join(build_page("NAVBAR_ADMIN.html")))
            continue
        elif value == "LISTA_ALUMNOS":
            alumnos = db_alumnos.getByQuery({"aula": kwargs["aula"].upper()})
            alumnos_output = [
                f'<tr><th scope="row"><a href="alumnos/{alumno["id"]}">{alumno["nombre"]}</a></th><td>{alumno["correo"]}</td><td>{alumno["telefono"]}</td><td><a class="btn btn-primary" href="mailto:{alumno["correo"]}">Enviar Correo</a> <a class="btn btn-danger" href="alumnos/{alumno["id"]}/delete">Borrar</a></td></tr>'
                for alumno in alumnos
            ]
            output += alumnos_output
            continue
        elif value == "LISTA_TAREAS":
            tareas = db_autotareas.getByQuery({"aula": kwargs["aula"].upper()})
            alumnos_output = [
                f'<tr><th scope="row"><a href="tareas/{alumno["id"]}">{alumno["tipo"]}: {alumno["nombre"]}</a></td><td>{" > ".join(alumno["alumno"])}</td><td><a class="btn btn-danger" href="tareas/{alumno["id"]}/delete">Borrar</a></td></tr>'
                for alumno in tareas
            ]
            output += alumnos_output
            continue
        elif value == "CHECK_ALUMNOS":
            alumnos = db_alumnos.getByQuery({"aula": kwargs["aula"].upper()})
            alumnos_output = [
                f'<div class="form-check"><input class="form-check-input" type="checkbox" value="{alumno["nombre"]}" id="cb-{alumno["id"]}" name="alumno"><label class="form-check-label" for="cb-{alumno["id"]}">{alumno["nombre"]}</label></div>'
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
                f'<tr><th scope="row">{dia["dia"]}</th><td>{dia["menu"].replace(chr(10), "<br>")}</td></tr>'
                for dia in kwargs["menu"]
            ]
            output += menu_output
        else:
            output.append(value)
            continue
    return output


@app.get("/aula/<aula>")
async def aula__index(req, aula: str):
    aula = aula.upper()
    if aula == "NEW":
        return "".join(build_page("aula/new.html", aula=aula)), HEADERS
    elif "_EDIT" in aula:
        eaula=aula.replace("_EDIT", "")
        return "".join(build_page("aula/edit.html", modo="edit_aula", aula=eaula)), HEADERS

    return "".join(build_page("aula/-/index.html", aula=aula)), HEADERS


@app.get("/aula")
async def aula__index(req):
    return "".join(build_page("aula.html")), HEADERS


@app.get("/aula/<aula>/soporte-tecnico")
async def aula__soportetecnico(req, aula: str):
    aula = aula.upper()
    return "".join(build_page("aula/-/soporte-tecnico.html", aula=aula)), HEADERS


@app.get("/aula/<aula>/tareas")
async def aula__tareas__all(req, aula: str):
    aula = aula.upper()
    return "".join(build_page("aula/-/tareas.html", aula=aula)), HEADERS

@app.get("/aula/<aula>/alumnos")
async def aula__alumnos__all(req, aula: str):
    aula = aula.upper()
    return "".join(build_page("aula/-/alumnos.html", aula=aula)), HEADERS

@app.get("/aula/<aula>/delete")
async def aula__delete(req, aula: str):
    db_aulas.deleteById(int(aula))
    return redirect("/aula")


@app.get("/aula/<aula>/alumnos/<id>")
async def aula__alumnos__get(req, aula: str, id):
    aula = aula.upper()
    if id == "new":
        return "".join(
            build_page("aula/-/alumnos/new.html", aula=aula, alumno_id=id)
        ), HEADERS
    return "".join(
        build_page("aula/-/alumnos/-.html", modo="edit_alumno", aula=aula, alumno_id=id)
    ), HEADERS

@app.get("/aula/<aula>/tareas/<id>")
async def aula__tareas__get(req, aula: str, id):
    aula = aula.upper()
    if id == "new":
        return "".join(
            build_page("aula/-/tareas/new.html", aula=aula, alumno_id=id)
        ), HEADERS
    return "".join(
        build_page("aula/-/tareas/-.html", modo="edit_tarea", aula=aula, tarea_id=id)
    ), HEADERS


@app.get("/aula/<aula>/alumnos/<id>/delete")
async def aula__alumnos__delete(req, aula: str, id):
    aula = aula.upper()
    db_alumnos.deleteById(int(id))
    return redirect(f"/aula/{aula}/alumnos")


@app.get("/aula/<aula>/menu-comedor")
async def aula__menu_comedor(req, aula: str):
    aula = aula.upper()
    hoy_iso = datetime.today().isoformat().split("T")[0]
    m = [{"dia": dia, "menu": menu[dia]} for dia in menu.keys()]
    return "".join(
        build_page(
            "aula/-/menu-comedor.html",
            aula=aula,
            menu=m,
            hoy=menu.get(hoy_iso, "Hoy no hay comedor, o no se ha descargado el menu."),
        )
    ), HEADERS


@app.post("/aula/<aula>/alumnos/<id>")
async def aula__alumnos__post(req, aula: str, id):
    aula = aula.upper()
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

@app.post("/aula/<aula>/tareas/<id>")
async def aula__tareas__post(req, aula: str, id):
    aula = aula.upper()
    if id == "new":
        db_autotareas.add(
            {
                "nombre": req.form["nombre"] or "No Definido",
                "tipo": req.form["tipo"] or "No Definido",
                "alumno": req.form.getlist("alumno") or [],
                "dow": req.form.getlist("dow") or [],
                "dif": req.form["dif"] or "0",
                "aula": aula,
            }
        )
    else:
        db_autotareas.updateById(
            int(id),
            {
                "nombre": req.form["nombre"] or "No Definido",
                "tipo": req.form["tipo"] or "No Definido",
                "alumno": req.form.getlist("alumno") or [],
                "dow": req.form.getlist("dow") or [],
                "dif": req.form["dif"] or "0",
                "aula": aula,
            }
        )

    return redirect(f"/aula/{aula}/tareas")


@app.get("/aula/<aula>/tareas/<id>/delete")
async def aula__tareas__delete(req, aula: str, id):
    aula = aula.upper()
    db_autotareas.deleteById(int(id))
    return redirect(f"/aula/{aula}/tareas")
@app.post("/aula/<aula>")
async def aula__post(req, aula: str):
    aula = aula.upper()
    if aula == "NEW":
        if db_aulas.getByQuery({"codigo": req.form["codigo"].upper()}) != []:
            return redirect(f"/_error/aula_code_used")
        db_aulas.add(
            {
                "codigo": req.form["codigo"].upper(),
                "nombre": req.form["nombre"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
            }
        )
        return redirect(f"/aula/{req.form["codigo"].upper()}")
    else:
        db_alumnos.updateByQuery(
            {"codigo": aula},
            {
                "nombre": req.form["nombre"] or "No Definido",
                "extra": req.form["extra"] or "No Definido",
            },
        )

    return redirect(f"/aula")


@app.get("/")
async def index(req):
    return "".join(build_page("index.html")), HEADERS

@app.get("/admin")
async def admin(req):
    print("Alguien ha accedido al panel de Admin ", end="")
    print(str(req.args.get("pin")), str(config.get("PinCode", "991199")))
    if str(req.args.get("pin")) == str(config.get("PinCode", "991199")):
        print("con credenciales validos")
        return "".join(build_page("admin.html", inputpin = str(req.args.get("pin")))), HEADERS
    print("con credenciales invalidos!!!!!!!")
    return redirect("/_error/incorrect_admin_pin")

@app.get("/admin/recargar_menu")
async def admin__recargar_menu(req):
    reload_comedor()
    return "Comedor Recargado, ya puedes cerrar esta pestaña."

@app.get("/aula_open")
async def aula_open(req):
    return redirect(f'/aula/{req.args.get("pin")}')

@app.get("/admin/ota_update")
async def admin__ota_update(req):
    print("Alguien ha accedido al panel de Admin ", end="")
    if req.args.get("pin") == config.get("PinCode", "991199"):
        print("con credenciales validos")
        ota_updater()
        return redirect("/admin#post_update")
    print("con credenciales invalidos!!!!!!!")
    return redirect("/_error/incorrect_admin_pin")

@app.get("/_error/incorrect_admin_pin")
async def error__incorrect_admin_pin(req):
    return "".join(build_page("_error/incorrect_admin_pin.html")), HEADERS

@app.get("/_error/aula_code_used")
async def error__aula_code_used(req):
    return "".join(build_page("_error/aula_code_used.html")), HEADERS



if __name__ == "__main__":
    reload_comedor()
    if config.get("PinCode", "991199") == "991199":
        print("     AVISO DE SEGURIDAD.     ")
        print("=============================")
        print(" PARA SERVIDORES COMPARTIDOS ")
        print(" Y SERVIDORES PUBLICOS       ")
        print("=============================")
        print(" Cambia el PinCode del       ")
        print(" config.yaml por otro        ")
        print("=============================")
    app.run(host="0.0.0.0", port=17170, debug=False)
