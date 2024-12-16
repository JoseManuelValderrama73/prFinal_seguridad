import sql, config

import os
from datetime import datetime


class Usuario:
    def __init__(self):
        self.logged_in = False

    def __getFechaHoy(self):
        return datetime.today()

    def creaSesion(self, nombre, maestra):
        if not os.path.exists(f"{config.DB_DIR}/{nombre}.db"):
            self.db = sql.SQL(nombre)
            self.db.insertar("maestra", nombre, maestra)
            self.logged_in = True
        else:
            raise NameError("Ya existe ese usuario")

    def iniciaSesion(self, nombre, maestra):
        self.db = sql.SQL(nombre)
        self.logged_in = maestra == self.db.getContrasena()
        return self.logged_in

    def cierraSesion(self):
        if self.logged_in:
            self.db.dbClose()
            self.logged_in = False
        else:
            raise SystemError("No hay sesion iniciada")

    def getUsuario(self, clave):
        if self.logged_in:
            f = self.db.getFila(clave)
            if f:
                return f[1]
            else:
                raise NameError("Esa clave no existe")
        else:
            raise SystemError("Se ha cerrado la sesion")

    def getContrasena(self, clave):
        if self.logged_in:
            return self.db.getContrasena(clave)
        else:
            raise SystemError("Se ha cerrado la sesion")

    def contrasenaPasada(self, clave):
        hoy = self.__getFechaHoy()

        f = datetime.strptime(self.getFecha(clave), "%d-%m-%Y")
        d = hoy - f
        return d.days > config.DIAS_AVISO

    def getFecha(self, clave):
        if self.logged_in:
            f = self.db.getFila(clave)
            if f:
                return f[3]
            else:
                raise NameError("Esa clave no existe")
        else:
            raise SystemError("Se ha cerrado la sesion")

    def guardar(self, clave, usuario, contrasena):
        if self.logged_in:
            self.db.insertar(clave, usuario, contrasena)
        else:
            raise SystemError("Se ha cerrado la sesion")

    def editar(self, clave, usuario="", contrasena=""):
        if self.logged_in:
            self.db.editar(clave, usuario, contrasena)
        else:
            raise SystemError("Se ha cerrado la sesion")

    def eliminar(self, clave):
        if self.logged_in:
            self.db.eliminar(clave)
        else:
            raise SystemError("Se ha cerrado la sesion")
