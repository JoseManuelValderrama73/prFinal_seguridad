from usuario import Usuario
import getpass
import os

directory = 

if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directorio {directory} creado")
else: 
    print(f"Directorio {directory} ya existe")


# imprime el texto en rojo
def error(s):
    print(f"\033[31m{s}\033[0m")


# imprime el texto en verde
def ok(s):
    print(f"\033[32m{s}\033[0m")


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

    return valida and len(pwd) >= 5


while True:
    ok("prueba")
    print("::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::: GESTOR DE COONTRASEÑAS ::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("0. SALIR")
    opcion = int(input("Introduce opción deseada: "))
    print("")

    if opcion == 1:
        u = Usuario()

        usu = input("Introduce el usuario: ")
        while True:
            passw = input("Introduce una contraseña: ")
            spassw = input("Introducela de nuevo: ")
            if passw != spassw:
                error("Las contraseñas no coinciden\n")
            else:
                if not comprobarContrasena(passw):
                    error("Contraseña invalida")
                    print("· Minimo 5 caracteres")
                    print("· Al menos una mayuscula")
                    print("· Al menos un numero (no al inicio)\n")
                else:
                    break

        try:
            u.creaSesion(usu, passw)
        except NameError as e:
            error(e)

        ok("Se ha creado el usuario correctamente ")
        del u

    elif int(opcion) == 2:
        u = Usuario()
        control = True

        while control:
            usu = input("Introdue el ususario: ")
            passw = getpass.getpass("Introduce la contraseña(oculta, no se muestra): ")

            try:
                u.iniciaSesion(usu, passw)
                control = False

            except NameError:
                error("Contraseña o usuario incorrectos ")
                control = True

        while True:
            print("")
            print("::::::::::::::::::::::::::::::::::::::::::::")
            print(":::::::::: GESTOR DE COONTRASEÑAS ::::::::::")
            print("::::::::::::::::::::::::::::::::::::::::::::")
            print("1. Consultar usuario de una contraseña")
            print("2. Consultar una contraseña")
            print("3. Consultar fecha límite de una contraseña")
            print("4. Guardar contraseña nueva")
            print("5. Editar una contraseña")
            print("6. Eliminar una contraseña")
            print("0. CERRAR SESIÓN")
            opcion = input("Elija opcion: ")
            print("")

            
            if(int(opcion) == 1):
                clave = input("Introduce la clave a consultar: ")
            
                try:
                    print(f"EL usuario es: {u.getUsuario(clave)}")
                except NameError as e:
                    print(e)

            elif(int(opcion) == 2):
                clave = input("Introduce la clave de la contraseña a consultar: ")
                if(u.contrasenaPasada(clave)):
                    print(f"La contraseña {u.getContrasena(clave)} debe ser cambiada ")
                else:
                    print(f"La contraseña es: {u.getContrasena(clave)}")

            elif(int(opcion) == 3):
                clave = input("Introduce la clave de la contraseña a consultar: ")
                print(f"La contraseña {u.getContrasena(clave)} es valida hasta {u.getFecha(clave)}")
                
            elif(int(opcion) == 4):
                clave = input("Introduce la clave(identificador de la contraseña que va a guardar): ")
                usu = input("Introduce el usuario de la contraseña que va a guardar: ")
                passw = input("Introduce la contraseña a guardar: ")

                u.guardar(clave, usu, passw)
                ok("Guardada con exito!")

            elif(int(opcion) == 5):
                clave = input("Introducir la clave de la contraseña a editar: ")
                usu = input("Introduce el nuevo usuario (N si no quieres editarlo): ")
                passw = input("Introduce la nueva contraseña (N si no quieres editarla): ")

                if(usu == "N"):
                    u.editar("", passw)
                    ok("Contraseña editada con éxito")
                elif(passw == "N"):
                    u.editar(usu, "")
                    ok("Usuario editado con éxito")
                elif(passw == "N" and usu == "N"):
                    error("Debe introducir al menos una de ellas")
                else:
                    u.editar(usu, passw)
                    ok("Usuario y contraseña editadas correctamente")

            elif(int(opcion) == 6):
                clave = input("Introduce la clave de la contraseña que desea eliminar: ")
                u.eliminar(clave)

                ok("La contraseña ha sido borrada con exito")

            elif(int(opcion) == 0):
                u.cierraSesion()
                ok("Sesión cerrada")
                print("")
                break

        
    elif(int(opcion) == 0):
        print("Hasta la proxima!")
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
