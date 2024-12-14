import sqlite3 as sql
import config


class SQL:
    def __init__(self):
        self.tipo_cifrado = config.CIFRADO
        self.logged_in = False
        self.lon = -1
        self.conexion = sql.connect(config.NOMBRE_DB)
        try:
            self.crear()
        except sql.OperationalError:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM t")
            datos = cursor.fetchall()
            for _ in datos:
                self.lon += 1

    def logIn(self, maestra):
        pwd = self.__encriptar(maestra)
        if self.lon == -1:
            self.insertar("maestra", "", pwd)

        if pwd == self.__getMaestra():
            self.logged_in = True
            return True
        else:
            return False

    def logOut(self):
        self.conexion.close()
        self.logged_in = False

    def crear(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """CREATE TABLE t (
                clave text,
                usuario text,
                contrasena text,
                cifrado integer
            )"""
        )
        self.conexion.commit()

    def __c1(self, pwd):
        return pwd

    def __c2(self, pwd):
        return pwd

    def __c3(self, pwd):
        return pwd

    def __encriptar(self, pwd):
        if self.tipo_cifrado == 1:
            return self.__c1(pwd)
        elif self.tipo_cifrado == 2:
            return self.__c2(pwd)
        elif self.tipo_cifrado == 3:
            return self.__c3(pwd)
        else:
            raise ValueError("El metodo de cifrado no es correcto")

    def __getMaestra(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM t WHERE clave='maestra'")
        return cursor.fetchall()[0][2]

    def getFila(self, clave):
        if self.logged_in:
            cursor = self.conexion.cursor()
            cursor.execute(f"SELECT * FROM t WHERE clave='{clave}'")
            dato = cursor.fetchall()
            if len(dato) == 0:
                return None
            else:
                return dato[0]
        else:
            raise SystemError("Se ha cerrado la sesion")

    def getLon(self):
        if self.logged_in:
            return self.lon
        else:
            raise SystemError("Se ha cerrado la sesion")

    def isLoggedIn(self):
        return self.logged_in

    def insertar(self, clave, usuario, contrasena):
        if self.logged_in:
            if self.getFila(clave):
                raise NameError("Esa clave ya existe")
            else:
                pwd = self.__encriptar(contrasena)

                cursor = self.conexion.cursor()
                cursor.execute(
                    f"INSERT INTO t VALUES ('{clave}', '{usuario}', '{pwd}', {self.tipo_cifrado})"
                )
                self.conexion.commit()
                self.lon += 1
        else:
            raise SystemError("Se ha cerrado la sesion")

    def editar(self, clave, usuario="", contrasena=""):
        if self.logged_in:
            if self.getFila(clave):
                cursor = self.conexion.cursor()
                if contrasena != "":
                    pwd = self.__encriptar(contrasena)
                    cursor.execute(
                        f"UPDATE t SET contrasena='{pwd}', cifrado={self.tipo_cifrado} WHERE clave='{clave}'"
                    )
                    self.conexion.commit()
                if usuario != "":
                    cursor.execute(
                        f"UPDATE t SET usuario='{usuario}' WHERE clave='{clave}'"
                    )
                    self.conexion.commit()
            else:
                raise NameError("Esa clave no existe")
        else:
            raise SystemError("Se ha cerrado la sesion")

    def eliminar(self, clave):
        if self.logged_in:
            if self.getFila(clave):
                self.getFila(clave)
                cursor = self.conexion.cursor()
                cursor.execute(f"DELETE FROM t WHERE clave='{clave}'")
                self.conexion.commit()
                self.lon -= 1
            else:
                raise NameError("Esa clave no existe")
        else:
            raise SystemError("Se ha cerrado la sesion")
