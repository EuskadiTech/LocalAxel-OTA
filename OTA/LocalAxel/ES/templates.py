TEMPLATES = {'aula/-/alumnos.html': 'START_PAGE~NAVBAR~ <div class=container style="padding-top: 60px;"> <h1>Alumnos</h1> <table class="table table-hover"> <thead> <tr class=table-success> <th scope=col>Nombre completo</th> <th scope=col>Correo</th> <th scope=col>Telefono</th> <th scope=col>Acciónes</th> </tr> </thead> <tbody> <tr> <th colspan=4><a href=alumnos/new>Crear Alumno</a></th> </tr> ~LISTA_ALUMNOS~ </tbody> </table> </div> ~END_PAGE', 'aula/-/alumnos/new.html': 'START_PAGE~NAVBAR~ <div class=container style="padding-top: 60px;"> <h1>Crear Alumno</h1> <form method=post> <fieldset> <legend>Alumno: Nuevo...</legend> <div> <label for=nombre_alumno class="form-label mt-4">Nombre</label> <input type=tel class=form-control id=nombre_alumno name=nombre placeholder="Introduce el nombre del alumno - obligatorio."> </div> <div> <label for=correo_alumno class="form-label mt-4">Correo Electronico</label> <input type=email class=form-control id=correo_alumno name=correo placeholder="Introduce el correo - o no, este campo solo es para los docentes, no se enviara ningun correo."> </div> <div> <label for=telefono_alumno class="form-label mt-4">Nº Telefono</label> <input type=tel class=form-control id=telefono_alumno name=telefono placeholder="Introduce el Numero de telefono - o no, este campo solo es para los docentes."> </div> <div> <label for=extra_alumno class="form-label mt-4">Datos Extra</label> <textarea class=form-control id=extra_alumno rows=3 name=extra></textarea> </div> <br> <button type=submit class="btn btn-primary">Guardar</button> </fieldset> </form> </div> ~END_PAGE', 'aula/-/alumnos/-.html': 'START_PAGE~NAVBAR~ <div class=container style="padding-top: 60px;"> <h1>Crear Alumno</h1> <form method=post> <fieldset> <legend>Alumno: ~ALUMNO_NOMBRE~</legend> <div> <label for=nombre_alumno class="form-label mt-4">Nombre</label> <input type=tel class=form-control id=nombre_alumno value=~ALUMNO_NOMBRE~ name=nombre placeholder="Introduce el nombre del alumno - obligatorio."> </div> <div> <label for=correo_alumno class="form-label mt-4">Correo Electronico</label> <input type=email class=form-control id=correo_alumno name=correo value=~ALUMNO_CORREO~ placeholder="Introduce el correo - o no, este campo solo es para los docentes, no se enviara ningun correo."> </div> <div> <label for=telefono_alumno class="form-label mt-4">Nº Telefono</label> <input type=tel class=form-control id=telefono_alumno name=telefono value=~ALUMNO_TELEFONO~ placeholder="Introduce el Numero de telefono - o no, este campo solo es para los docentes."> </div> <div> <label for=extra_alumno class="form-label mt-4">Datos Extra</label> <textarea class=form-control id=extra_alumno rows=3 name=extra>~ALUMNO_EXTRA~</textarea> </div> <br> <button type=submit class="btn btn-primary">Guardar</button> </fieldset> </form> </div> ~END_PAGE', 'aula/-/menu-comedor.html': 'START_PAGE~NAVBAR~ <div class=container style="padding-top: 60px;"> <h1>Menu Comedor</h1> <h2>Hoy</h2> <b>~MENU_COMEDOR_HOY~</b> <h2>Mantenimiento</h2> <b>En el primer dia del mes: </b> Si no ves los datos de este mes (o en servidores 24/7): Haz click en <a href=/admin/recargar_menu class="btn btn-warning btn-sm">Recargar Comedor</a> para descargar el menú desde EuskadiTech <h2>Este mes</h2> <table class="table table-hover"> <thead> <tr class=table-success> <th scope=col>Dia</th> <th scope=col>Menu</th> </tr> </thead> <tbody> ~MENU_COMEDOR_TABLA~ </tbody> </table> </div> ~END_PAGE', 'START-PAGE.html': '<!doctype html><html lang=es> <head><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1"><title>LocalAxel</title><link rel="shortcut icon" href=/static/icons__favicon.ico type=image/x-icon><link href=https://bootswatch.com/5/spacelab/bootstrap.min.css rel=stylesheet></head> <body>', 'END-PAGE.html': '<script src=https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js integrity=sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz crossorigin=anonymous></script> </body> </html>', 'NAVBAR.html': '<nav class="navbar navbar-expand-lg bg-success" data-bs-theme=dark> <div class=container> <a class=navbar-brand href=/aula>Axel Aula</a> <button class=navbar-toggler type=button data-bs-toggle=collapse data-bs-target=#navbarColor01 aria-controls=navbarColor01 aria-expanded=false aria-label="Toggle navigation"> <span class=navbar-toggler-icon></span> </button> <div class="collapse navbar-collapse" id=navbarColor01> <ul class="navbar-nav me-auto"> <li class=nav-item> <a class=nav-link href=/aula/~CODIGO_AULA~/index>Inicio</a> </li> <li class=nav-item> <a class=nav-link href=/aula/~CODIGO_AULA~/alumnos>Alumnos</a> </li> <li class=nav-item> <a class=nav-link href=/aula/~CODIGO_AULA~/menu-comedor>Menu Comedor</a> </li> <li class=nav-item> <a class=nav-link href=/aula/~CODIGO_AULA~/soporte-tecnico>Soporte Tecnico</a> </li> </ul> <div class=d-flex> <a class="btn btn-secondary my-2 my-sm-0" href=/admin>Administrar Servidor</a> </div> </div> </div> </nav>'}
FILES = ['static__fonts__icomoon.eot', 'static__fonts__icomoon.svg', 'static__fonts__icomoon.ttf', 'static__fonts__icomoon.woff', 'static__icons__512x512.png', 'static__icons__favicon.ico', 'static__img__logo.png', 'static__img__bgpattern.jpg']
