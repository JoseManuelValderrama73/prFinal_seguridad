from usuario import Usuario
import config

import getpass, os, sys, datetime


# imprime el texto en rojo
def error(s):
    print(f"\033[31m{s}\033[0m")


# imprime el texto en verde
def ok(s):
    print(f"\033[32m{s}\033[0m")


# imprime el texto en verde
def advertencia(s):
    print(f"\033[33m{s}\033[0m")


def comprobarContrasena(pwd):
    valida = False
    for i in range(0, len(pwd)):
        if pwd[i].isupper():
            valida = True
            break
        elif pwd[i].isdigit():
            if i != 0:
                valida = True
            break

    for letra in pwd:
        if letra == "ñ":
            valida = False
            break

    return valida and len(pwd) >= 5


def comprobarNombreUsuario(pwd):
    valida = True
    for letra in pwd:
        if letra == "ñ":
            valida = False
            break

    return valida and not pwd[0].isdigit()


if not os.path.exists(config.DB_DIR):
    os.makedirs(config.DB_DIR)

while True:
    print("::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::: GESTOR DE COONTRASEÑAS ::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("0. SALIR")
    opcion = int(input("Introduce opción deseada: "))
    print("\n")
    u = Usuario()

    if opcion == 0:
        print("Hasta la proxima!")
        break

    elif opcion == 1:
        while True:
            usu = input("Introduce el usuario: ")
            if not comprobarNombreUsuario(usu):
                error("Nombre de usuario invalido")
                print("· No debe contener 'ñ'")
                print("· No debe haber un numero al inicio\n")
            else:
                break
        while True:
            passw = input("Introduce una contraseña: ")
            if not comprobarContrasena(passw):
                error("Contraseña invalida")
                print("· Minimo 5 caracteres")
                print("· Al menos una mayuscula")
                print("· Al menos un numero (no al inicio)\n")
            spassw = input("Introducela de nuevo: ")
            if passw != spassw:
                error("Las contraseñas no coinciden\n")
            else:
                break

        try:
            u.creaSesion(usu, passw)
        except NameError as e:
            error(e)

        ok("Se ha creado el usuario correctamente ")

    elif opcion == 2:
        while True:
            usu = input("Introdue el ususario: ")
            if not os.path.exists(f"{config.DB_DIR}/{usu}.db"):
                error("No existe un usuario con ese nombre")
            else:
                break
        intentos = 3
        while True:
            passw = getpass.getpass("Introduce la contraseña (oculta, no se muestra): ")

            if u.iniciaSesion(usu, passw):
                break
            else:
                intentos -= 1
                if intentos == 0:
                    error("Contraseña incorrecta. No quedan mas intentos")
                    sys.exit()
                else:
                    error(f"Contraseña incorrecta. Quedan {intentos} intentos")

    if u.logged_in:
        while True:
            print("\n::::::::::::::::::::::::::::::::::::::::::::")
            print(":::::::::: GESTOR DE COONTRASEÑAS ::::::::::")
            print("::::::::::::::::::::::::::::::::::::::::::::")
            print("1. Consultar una contraseña")
            print("2. Ver lista de las claves")
            print("3. Consultar fecha límite de una contraseña")
            print("4. Guardar contraseña nueva")
            print("5. Editar una contraseña")
            print("6. Eliminar una contraseña")
            print("0. CERRAR SESIÓN")
            opcion = int(input("Elija opcion: "))
            print("\n")

            if opcion == 1:
                clave = input("Introduce la clave a consultar: ")

                try:
                    print(
                        f"{clave}: Usuario: {u.getUsuario(clave)}, Contraseña: {u.getContrasena(clave)}, Creación: {u.getFecha(clave)}"
                    )
                    if u.contrasenaPasada(clave):
                        advertencia(
                            f"Han pasado más de {config.DIAS_AVISO} dias desde que se creó la clave,\ndebería ser cambiada"
                        )
                except NameError as e:
                    error(e)

            elif opcion == 2:
                lista = u.getListaClaves()
                print("Las claves guardadas son:")
                for clave in lista:
                    print(" - ", clave)

            elif opcion == 3:
                clave = input("Introduce la clave de la contraseña a consultar: ")
                f = datetime.datetime.strptime(
                    u.getFecha(clave), "%d-%m-%Y"
                ) + datetime.timedelta(days=config.DIAS_AVISO)
                print(
                    f"La contraseña {u.getContrasena(clave)} es valida hasta {f.strftime("%d-%m-%Y")}"
                )

            elif opcion == 4:
                clave = input(
                    "Introduce la clave(identificador de la contraseña que va a guardar): "
                )
                usu = input("Introduce el usuario de la contraseña que va a guardar: ")
                passw = input("Introduce la contraseña a guardar: ")

                u.guardar(clave, usu, passw)
                ok("Guardada con exito!")

            elif opcion == 5:
                clave = input("Introducir la clave de la contraseña a editar: ")
                usu = input(
                    "Introduce el nuevo usuario (vacio si no quieres editarlo): "
                )
                passw = input(
                    "Introduce la nueva contraseña (vacio si no quieres editarla): "
                )

                if passw == "" and usu == "":
                    advertencia("No se ha editado nada")
                else:
                    u.editar(clave, usu, passw)
                    ok("Se ha editado con éxito")

            elif opcion == 6:
                clave = input(
                    "Introduce la clave de la contraseña que desea eliminar: "
                )
                u.eliminar(clave)

                ok("La contraseña ha sido borrada con exito")

            elif opcion == 0:
                u.cierraSesion()
                ok("Sesión cerrada\n")
                break


"""
u = Usuario()
print("prueba")
u.iniciaSesion("valde", "qwerty")
# u.creaSesion("valde", "qwerty")
# u.guardar("uja", "jmvs0008", "1234")
# u.guardar("personal", "josemvalde", "asdf")

# u.eliminar("uja")
u.editar("personal", contrasena="zxc")
print(u.getContrasena("personal"))
u.cierraSesion()
"""
