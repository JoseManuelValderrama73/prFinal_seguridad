from sql import SQL

sql = SQL()
sql.logIn("qwerty")
# sql.crear("qwerty")
# sql.insertar("uja", "jmvs0008@red.ujaen.es", "12340")
# sql.insertar("icloud", "josemvalde@icloud.com", "qwert")
# sql.eliminar("icloud")
dato = sql.getFila("icloud")
if dato:
    print(dato[2])
else:
    print("no")

print(sql.getLon())
