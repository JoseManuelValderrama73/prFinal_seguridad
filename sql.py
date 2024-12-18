import sqlite3 as sql
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64, os

import config


class SQL:
    def __init__(self, nombre):
        self.key = nombre
        self.lon = -1
        if not os.path.exists(config.DB_DIR):
            raise NameError("El directorio especificado en config.py no es valido")
        self.conexion = sql.connect(f"{config.DB_DIR}/{nombre}.db")
        try:
            self.__crear()
        except sql.OperationalError:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM t")
            datos = cursor.fetchall()
            for _ in datos:
                self.lon += 1

    def __crear(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            """CREATE TABLE t (
                clave text,
                usuario text,
                contrasena text,
                fecha text
            )"""
        )
        self.conexion.commit()

    # metodos de encriptar
    # 1. AES (Advanced Encryption Standard) with a Key and Salt
    def __encriptar(self, pwd):
        # Generate a salt
        salt = get_random_bytes(16)
        # Derive a key using PBKDF2
        key = PBKDF2(self.key, salt, dkLen=32, count=100000)
        # Create an AES cipher
        cipher = AES.new(key, AES.MODE_GCM)
        # Encrypt the password
        ciphertext, tag = cipher.encrypt_and_digest(pwd.encode())
        # Return salt, nonce, tag, and ciphertext (needed for decryption)
        return base64.b64encode(salt + cipher.nonce + tag + ciphertext).decode()

    # 1. AES (Advanced Encryption Standard) with a Key and Salt
    def __desencriptar(self, pwd):
        data = base64.b64decode(pwd)
        salt, nonce, tag, ciphertext = data[:16], data[16:32], data[32:48], data[48:]
        # Derive the key again
        key = PBKDF2(self.key, salt, dkLen=32, count=100000)
        # Recreate the AES cipher
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        # Decrypt the password
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def __getFechaHoy(self):
        return datetime.today()

    def getFila(self, clave):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT * FROM t WHERE clave='{clave}'")
        dato = cursor.fetchall()
        if len(dato) == 0:
            return None
        else:
            return dato[0]

    def getContrasena(self, clave="maestra"):
        f = self.getFila(clave)
        if f:
            return self.__desencriptar(f[2])
        else:
            raise NameError("Esa clave no existe")

    def getListaClaves(self):
        lista = []
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM t")
        datos = cursor.fetchall()
        for dato in datos:
            lista.append(dato[0])
        return lista

    def dbClose(self):
        self.conexion.close()

    def insertar(self, clave, usuario, contrasena):
        if self.getFila(clave):
            raise NameError("Esa clave ya existe")
        pwd = self.__encriptar(contrasena)

        cursor = self.conexion.cursor()
        cursor.execute(
            f"INSERT INTO t VALUES ('{clave}', '{usuario}', '{pwd}', '{self.__getFechaHoy().strftime("%d-%m-%Y")}')"
        )
        self.conexion.commit()
        self.lon += 1

    def editar(self, clave, usuario, contrasena):
        if clave == "maestra":
            raise NameError("Esa clave no es valida")
        if self.getFila(clave):
            cursor = self.conexion.cursor()
            if contrasena != "":
                pwd = self.__encriptar(contrasena)
                cursor.execute(
                    f"UPDATE t SET contrasena='{pwd}', fecha='{self.__getFechaHoy().strftime("%d-%m-%Y")}' WHERE clave='{clave}'"
                )
                self.conexion.commit()
            if usuario != "":
                cursor.execute(
                    f"UPDATE t SET usuario='{usuario}', fecha='{self.__getFechaHoy().strftime("%d-%m-%Y")}' WHERE clave='{clave}'"
                )
                self.conexion.commit()
        else:
            raise NameError("Esa clave no existe")

    def eliminar(self, clave):
        if clave == "maestra":
            raise NameError("Esa clave no es valida")
        if self.getFila(clave):
            cursor = self.conexion.cursor()
            cursor.execute(f"DELETE FROM t WHERE clave='{clave}'")
            self.conexion.commit()
            self.lon -= 1
        else:
            raise NameError("Esa clave no existe")
