import correo_recuperacion
from usuario import Usuario
import config

import getpass, os, sys, datetime, random, string


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


def recuperarContrasenaMaestra():
    email = input("Introduzca su correo electronico: ")
    codigo = correo_recuperacion.recuperar_clave(email)
    if codigo == input("Introduce el codigo de seguridad recibido por correo: "):
        print("Su contraseña es", u.getContrasena("maestra"))
    else:
        error("Codigo incorrecto")
        sys.exit()


def comprobarNombreUsuario(pwd):
    valida = True
    for letra in pwd:
        if letra == "ñ":
            valida = False
            break

    return valida and not pwd[0].isdigit()


def generar():
    if config.C_LON < 4:  # Ensure minimum length for complexity
        raise ValueError("La longitud de la contraseña no puede ser menor a 4")

    # Create pools of characters
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Ensure the password has at least one of each character type
    all_characters = lower + upper + digits + symbols
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols),
    ]

    # Fill the rest of the password length with random choices from all characters
    password += random.choices(all_characters, k=config.C_LON - 4)

    # Shuffle the password to make it random
    random.shuffle(password)

    return "".join(password)


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
            usu = input("Introduce el usuario: ")
            if not os.path.exists(f"{config.DB_DIR}/{usu}.db"):
                error("No existe un usuario con ese nombre")
            else:
                break
        intentos = 3
        while True:
            passw = getpass.getpass(
                "Introduce la contraseña (oculta, no se muestra) (intruduzca 'h' si la ha olvidado): "
            )
            if passw == "h":
                confi = input("¿Desea recuperar su contraseña? (s/n): ")
                if confi == "s":
                    recuperarContrasenaMaestra()
                else:
                    print("0K")
            else:
                if u.iniciaSesion(usu, passw):
                    break
                else:
                    intentos -= 1
                    if intentos == 0:
                        error("Contraseña incorrecta. No quedan mas intentos")
                        confi = input("¿Desea recuperar su contraseña? (s/n): ")
                        if confi == "s":
                            recuperarContrasenaMaestra()
                            intentos = 3
                        else:
                            print("0K")
                            sys.exit()
                    else:
                        error(f"Contraseña incorrecta. Quedan {intentos} intentos")
    else:
        error("Esa opción no es valida")

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
                        f"{clave}: Usuario: {u.getUsuario(clave)}, Contraseña: {u.getContrasena(clave)}, Creación / Última modificación: {u.getFecha(clave)}"
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
                    "Introduce la clave (identificador de la contraseña que va a guardar): "
                )
                usu = input("Introduce el usuario de la contraseña que va a guardar: ")
                while True:
                    passw = input(
                        "Introduce la contraseña a guardar ('g' para genererar una contraseña aleatoria): "
                    )
                    if passw == "g":
                        while True:
                            try:
                                passw = generar()
                                if (
                                    input(
                                        f"¿Quieres guardar la contraseña {passw}? (s, n): "
                                    )
                                    == "s"
                                ):
                                    break
                            except ValueError as e:
                                error(e)
                                print("Cambie la longitud en 'config.py'")
                                break

                    if passw == "":
                        error("La contraseña no puede estar vacía")
                    else:
                        break

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
            else:
                error("Esa opción no es valida")


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
