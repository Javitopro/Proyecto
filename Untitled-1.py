import sqlite3

def CrearBD():
    conexion = sqlite3.connect('biblio.db')
    conexion.execute('''CREATE TABLE `Alumnes` (
    `AlumneID` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Nombre` TEXT NOT NULL,
    `Telefono` INTEGER,
    `Direccion` TEXT NOT NULL
    );''')
    conexion.execute('''CREATE TABLE `Autores` (
    `AutorId` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Nombre` TEXT NOT NULL
    );''')
    conexion.execute('''CREATE TABLE `Libros` (
    `LibroId` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Titulo` TEXT NOT NULL,
    `ISBN` INTEGER NOT NULL,
    `Editorial` TEXT NOT NULL,
    `Paginas` INTEGER
    );''')
    conexion.execute('''CREATE TABLE `Ejemplares` (
    `EjemplarId` INTEGER PRIMARY KEY AUTOINCREMENT,
    `Localizacion` TEXT NOT NULL,
    `LibroId` INTEGER NOT NULL,
    FOREIGN KEY (`LibroId`) REFERENCES `Libros` (`LibroId`)
    );''')
    conexion.execute('''CREATE TABLE `Escribe` (
    `EscribeId` INTEGER PRIMARY KEY AUTOINCREMENT,
    `AutorId` INTEGER NOT NULL,
    `LibroId` INTEGER NOT NULL,
    FOREIGN KEY (`AutorId`) REFERENCES `Autores` (`AutorId`),
    FOREIGN KEY (`LibroId`) REFERENCES `Libros` (`LibroId`)
    );''')
    conexion.execute('''CREATE TABLE `Saca` (
    `PrestamoId` INTEGER PRIMARY KEY AUTOINCREMENT,
    `EjemplarId` INTEGER NOT NULL,
    `AlumneId` INTEGER NOT NULL,
    `FechaPrestamo` DATE NOT NULL,
    `FechaDevolucion` DATE NOT NULL,
    FOREIGN KEY (`EjemplarId`) REFERENCES `Ejemplares` (`EjemplarId`),
    FOREIGN KEY (`AlumneId`) REFERENCES `Alumnes` (`AlumneID`)
    );''')
    conexion.close()

def MostrarLibros():
    conexion = sqlite3.connect('biblio.db')
    registros=conexion.execute("SELECT * FROM Libros")
    print("\nTABLA LIBROS:")
    for i in registros:
        Id, Titulo,Isbn,Editorial,Paginas= i
        print("ID: ", Id, ". Titulo: ", Titulo, ". ISBN: ", Isbn, ". Editorial: ", Editorial, ". Paginas: ", Paginas,)
    conexion.close()

def MostrarEjemplares():
    conexion = sqlite3.connect('biblio.db')
    registros=conexion.execute("SELECT * FROM Ejemplares")
    print("\nTABLA EJEMPLARES:")
    for i in registros:
        Id, Localizacion,Libroid= i
        print("ID: ", Id, ". Localización: ", Localizacion, ". LibroID: ", Libroid,)
    conexion.close()

def MostrarAutores():
    conexion = sqlite3.connect('biblio.db')
    registros=conexion.execute("SELECT * FROM Autores")
    print("\nTABLA AUTORES:")
    for i in registros:
        Id, Nombre= i
        print("ID: ", Id, ". Nombre: ", Nombre,)
    conexion.close()

def MostrarAlumnos():
    conexion = sqlite3.connect('biblio.db')
    registros=conexion.execute("SELECT * FROM Alumnes")
    print("\nTABLA ALUMNOS:")
    for i in registros:
        Id, Nombre,Telefono,Direccion= i
        print("ID: ", Id, ". Nombre: ", Nombre, ". Teléfono: ", Telefono, ". Dirección: ", Direccion,)
    conexion.close()

def MostrarPrestamos():
    conexion = sqlite3.connect('biblio.db')
    registros=conexion.execute("SELECT * FROM Saca")
    print("\nTABLA PRÉSTAMOS:")
    for i in registros:
        Id, EjemplarId,AlumneId,FechaPrestamo,FechaDevolucion= i
        print("ID: ", Id, ". EjemplarID: ", EjemplarId, ". AlumneID: ", AlumneId, ". Fecha de préstamo: ", FechaPrestamo, ". Fecha de devolución: ", FechaDevolucion,)
    conexion.close()


#Gestionar els llibres, amb els seus exemplars i autors, de què disposa el centre. Aquesta part suposaria la gestió del catàleg del centre. 
#Gestionar els socis (alumnes) subscrits al servei de biblioteca.
#Gestionar els préstecs i devolucions que realitzen diàriament els socis.


def Accio():
    return int(input("Qué quieres hacer? \n -Agregar (1) \n -Eliminar (2) \n -Modificar (3) \n -Mostrar (4) \n"))

def GestionLibros():
    conexion = sqlite3.connect('biblio.db')
    cursor=conexion.cursor()
    accio=Accio()
    if(accio==1):
        respuesta=int(input("En Libros, Ejemplares o en Ambos? \n -Libros (1) \n -Ejemplares (2) \n -Ambos (3) \n"))
        if(respuesta==1 or respuesta==3):
            MostrarLibros()
            Título= input("Dime el título del libro: ")
            cursor.execute("SELECT LibroId FROM Libros WHERE Titulo=?", (Título,))
            existe=cursor.fetchone()
            if(existe==None):
                ISBN= int(input("Dime el código ISBN del libro: "))
                Editorial= input("Dime la editorial del libro: ")
                Páginas= int(input("Dime cuántas páginas tiene el libro: "))
                libro= (Título, ISBN, Editorial, Páginas)
                cursor.execute("INSERT INTO Libros(Titulo, ISBN, Editorial, Paginas) VALUES(?,?,?,?)",libro)
                LibroId=cursor.lastrowid #te da el ID de la fila que acabas de insertar (last row id)
                print(f"Libro '{Título}' insertado con éxito, ID: {LibroId}")
                
                MostrarAutores()
                Autor=input("Dime el nombre del autor: ")
                cursor.execute("SELECT AutorId FROM Autores WHERE Nombre=?", (Autor,))
                existe=cursor.fetchone()
                if(existe==None):
                    cursor.execute("INSERT INTO Autores(Nombre) VALUES(?)",(Autor,))
                    AutorId=cursor.lastrowid
                    print(f"Autor '{Autor}' insertado con éxito, ID: {AutorId}")
                else:
                    AutorId=existe[0]
                    print(f"Ya existe y el ID es {AutorId}")

                cursor.execute("INSERT INTO Escribe(AutorId, LibroId) VALUES(?, ?)", (AutorId, LibroId))
                conexion.commit()
            else:
                print("Ese libro ya existe")

        if(respuesta==2 or respuesta==3):
            MostrarLibros()
            MostrarEjemplares()
            if(respuesta==3):
                print("Ahora añadiremos los ejemplares")

            LibroId= int(input("Dime el ID del libro al cual pertenecerán los ejemplares: "))
            cursor.execute("SELECT * FROM Libros WHERE LibroId=?", (LibroId,))
            existe=cursor.fetchone()
            if(existe!=None):
                num=int(input("Cuantos ejemplares quieres añadir de este libro? "))
                for i in range(num):
                    i+=1
                    Localizacion= input("Dime la localización del ejemplar: ")  
                    ejemplar =(Localizacion, LibroId)
                    conexion.execute("INSERT INTO Ejemplares(Localizacion,LibroId) VALUES(?,?)",ejemplar)
                    conexion.commit()
            else:
                print("No existe ese libro")
        
        if(respuesta!=1 and respuesta!=2 and respuesta!=3):
            print("Esta no es una de las opciones")

        conexion.close()
        Pregunta()
        
    elif(accio==2):
        respuesta=int(input("Autor, Libros y Ejemplares, Libro y Ejemplares, o solo Ejemplares? \n -Autor, Libros y Ejemplares (1) \n -Libro y Ejemplares (2) \n -Ejemplares (3) \n"))
        if(respuesta==1):
            MostrarAutores()
            Autor=input("Inserta el nombre del autor que deseas eliminar: ")
            cursor.execute("SELECT AutorId FROM Autores WHERE Nombre=?", (Autor,))
            existe=cursor.fetchone()
            if(existe!=None):
                conexion.execute("DELETE FROM Ejemplares WHERE LibroId IN (SELECT LibroId FROM Escribe WHERE AutorId IN(SELECT AutorId FROM Autores WHERE Nombre=(?)))", (Autor,))
                conexion.execute("DELETE FROM Libros WHERE LibroId IN (SELECT LibroId FROM Escribe WHERE AutorId IN(SELECT AutorId FROM Autores WHERE Nombre=(?)))", (Autor,))
                conexion.execute("DELETE FROM Escribe WHERE AutorId IN (SELECT AutorId FROM Autores WHERE Nombre=(?))", (Autor,))
                conexion.execute("DELETE FROM Autores WHERE Nombre=(?)", (Autor,))
                conexion.commit()
                print("Eliminado correctamente.")
            else:
                print(f"No existe {Autor}")

        if(respuesta==2):
            MostrarLibros()
            Titulo=input("Inserta el título del libro que deseas eliminar: ")
            cursor.execute("SELECT LibroId FROM Libros WHERE Titulo=?", (Título,))
            existe=cursor.fetchone()
            if(existe!=None):
                conexion.execute("DELETE FROM Ejemplares WHERE LibroId IN (SELECT LibroId FROM Libros WHERE Titulo = ?)", (Titulo,))
                conexion.execute("DELETE FROM Escribe WHERE LibroId IN (SELECT LibroId FROM Libros WHERE Titulo = ?)", (Titulo,))
                conexion.execute("DELETE FROM Libros WHERE Titulo = ?", (Titulo,))
                conexion.commit()
                print("Eliminado correctamente.")
            else:
                print(f"No existe {Titulo}")
            
        if(respuesta==3):
            MostrarEjemplares()
            Ejemplar=int(input("Inserta el id del ejemplar que deseas eliminar: "))
            cursor.execute("SELECT EjemplarId FROM Ejemplares WHERE EjemplarId=?", (Ejemplar,))
            existe=cursor.fetchone()
            if(existe!=None):
                conexion.execute("DELETE FROM Ejemplares WHERE EjemplarId = ?", (Ejemplar,))
                conexion.commit()
                print("Eliminado correctamente.")
            else:
                print(f"No existe el ejemplar {Ejemplar}")   

        if(respuesta!=1 and respuesta!=2 and respuesta!=3):
            print("Esta no es una de las opciones")

        conexion.close()
        Pregunta()

    elif(accio==3):
        opcion=int(input("Qué quieres modificar? \n -Libro (1) \n -Ejemplar (2) \n -Autor (3) \n"))
        if(opcion==1):
            MostrarLibros()
            LibroId= int(input("Dime el ID del libro que quieres modificar: "))
            cursor.execute("SELECT * FROM Libros WHERE LibroId=?", (LibroId,))
            existe=cursor.fetchone()
            if(existe!=None):
                nuevo_titulo= input("Dime el nuevo título del libro: ")
                nuevo_ISBN= int(input("Dime el nuevo código ISBN del libro: "))
                nueva_editorial= input("Dime la nueva editorial del libro: ")
                nuevas_paginas= int(input("Dime cuántas páginas tiene el libro: "))
                conexion.execute("UPDATE Libros SET Titulo=?, ISBN=?, Editorial=?, Paginas=? WHERE LibroId=?", (nuevo_titulo, nuevo_ISBN, nueva_editorial, nuevas_paginas, LibroId))
                conexion.commit()
                print("Modificado correctamente.")
            else:
                print("No existe ese libro")

        if(opcion==2):
            MostrarEjemplares()
            EjemplarId= int(input("Dime el ID del ejemplar que quieres modificar: "))
            cursor.execute("SELECT * FROM Ejemplares WHERE EjemplarId=?", (EjemplarId,))
            existe=cursor.fetchone()
            if(existe!=None):
                nueva_localizacion= input("Dime la nueva localización del ejemplar: ")
                conexion.execute("UPDATE Ejemplares SET Localizacion=? WHERE EjemplarId=?", (nueva_localizacion, EjemplarId))
                conexion.commit()
                print("Modificado correctamente.")
            else:
                print("No existe ese ejemplar")

        if(opcion==3):
            MostrarAutores()
            AutorId= int(input("Dime el ID del autor que quieres modificar: "))
            cursor.execute("SELECT * FROM Autores WHERE AutorId=?", (AutorId,))
            existe=cursor.fetchone()
            if(existe!=None):
                nuevo_nombre= input("Dime el nuevo nombre del autor: ")
                conexion.execute("UPDATE Autores SET Nombre=? WHERE AutorId=?", (nuevo_nombre, AutorId))
                conexion.commit()
                print("Modificado correctamente.")
            else:
                print("No existe ese autor")
        conexion.close()
        Pregunta()
    
    elif(accio==4):
        resposta=int(input("Libros, Ejemplares o Autores? \n -Libros (1) \n -Ejemplares (2) \n -Autores (3) \n"))
        if(resposta==1):
            MostrarLibros()
        elif(resposta==2):
            MostrarEjemplares()
        elif(resposta==3):
            MostrarAutores()
        else:
            print("Esta no es una de las opciones")            
        Pregunta()

    else:
        print("Esta no es una de las opciones")
        Accio()
    

def GestionAlumnos():
    conexion = sqlite3.connect('biblio.db')
    cursor=conexion.cursor()
    accio=Accio()
    if(accio==1):
        Nombre= input("Dime el nombre del alumno: ")
        cursor.execute("SELECT AlumneID FROM Alumnes WHERE Nombre=?", (Nombre,))
        existe=cursor.fetchone()
        if(existe==None):
            Telefono= int(input("Dime el teléfono del alumno: "))
            Direccion= input("Dime la dirección del alumno: ")
            alumno= (Nombre, Telefono, Direccion)
            cursor.execute("INSERT INTO Alumnes(Nombre, Telefono, Direccion) VALUES(?,?,?)",alumno)
            conexion.commit()
        else:
            print("Ese alumno ya existe")
        conexion.close()
        Pregunta()

def GestionPrestamos():
    conexion = sqlite3.connect('biblio.db')
    cursor=conexion.cursor()
    accio=Accio()
    if(accio==1):
        MostrarEjemplares()
        MostrarAlumnos()
        EjemplarId= int(input("Dime el ID del ejemplar que se ha prestado: "))
        cursor.execute("SELECT EjemplarId FROM Ejemplares WHERE EjemplarId=?", (EjemplarId,))
        existe=cursor.fetchone()
        if(existe!=None):
            AlumneId= int(input("Dime el ID del alumno que ha cogido el ejemplar: "))
            cursor.execute("SELECT AlumneId FROM Alumnes WHERE AlumneId=?", (AlumneId,))
            existe=cursor.fetchone()
            if(existe!=None):
                FechaPrestamo= input("Dime la fecha de préstamo (YYYY-MM-DD): ")
                FechaDevolucion= input("Dime la fecha de devolución (YYYY-MM-DD): ")
                prestamo= (EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion)
                cursor.execute("INSERT INTO Saca(EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion) VALUES(?,?,?,?)",prestamo)
                conexion.commit()
            else:
                print("Ese alumno no existe")
        else:
            print("Ese ejemplar no existe")
        conexion.close()
        Pregunta()

    elif(accio==2):
        MostrarPrestamos()
        PrestamoId= int(input("Dime el ID del préstamo que quieres eliminar: "))
        cursor.execute("SELECT PrestamoId FROM Saca WHERE PrestamoId=?", (PrestamoId,))
        existe=cursor.fetchone()
        if(existe!=None):
            conexion.execute("DELETE FROM Saca WHERE PrestamoId = ?", (PrestamoId,))
            conexion.commit()
            print("Eliminado correctamente.")
        else:
            print(f"No existe el préstamo {PrestamoId}")
        conexion.close()
        Pregunta()

    elif(accio==3):
        print("lascosas")

def Pregunta():
    taula=int(input("Qué quieres gestionar? \n -Salir (0) \n -Libros/Ejemplares (1) \n -Socios (2) \n -Préstamos (3) \n -Crear BD (4) \n"))
    if(taula==1):
        GestionLibros()

    elif(taula==2):
        GestionAlumnos()

    elif(taula==3):
        GestionPrestamos()

    elif(taula==4):
        CrearBD()

    elif(taula==0):
        return

    else:
        print("Esta no es una de las opciones")
        Pregunta()

Pregunta()
