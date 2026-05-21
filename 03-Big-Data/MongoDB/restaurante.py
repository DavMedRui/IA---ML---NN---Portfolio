# Importar la librería JSON
import json
# Importar datetime
from datetime import datetime, timezone
# Importamos la clase para conectarnos a la base de datos
from MongoDBConector import MongoDBConector


def mostrarMenu():
    print("\nMENÚ DE OPCIONES")
    print("0 - Salir")
    print("1 - Abrir conexión")
    print("2 - Cargar JSON de documentos en MongoDB")
    print("3 - Mostrar los restaurantes dado un código postal")
    print("4 - Mostrar los restaurantes cuyo nombre o distrito empiecen por la cadena introducida")
    print("5 - Mostrar el número de restaurante que hay por tipo de cocina (ordenador de mayor a menor número)")
    print("6 - Mostrar los cinco restaurantes con mejor calificación promedio")
    print("7 - Introducir una nueva inspección a un restaurante")
    print("8 - Mostrar los 3 distritos con más restaurantes")
    print("9 - Borrar todos los dodumentos")
    print("10 - Cerrar conexión")

# Función del programa principal
def main():
    continuar = True
    conexion = None
    nombreColeccion = "restaurantes"
    
    conector = MongoDBConector("_", 0,"_","_","_","_")
   
    while continuar:
        
        
        mostrarMenu()
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                # Finalizar el programa sin usar el break
                print ("0")
                continuar = False


            case "1":
                # Crear la conexión a la BBDD y guardar en variable
                print ("1")
                conexion = conector.conectar()

            case "2":
                # Cargar el fichero JSON y realizar el insert a la base de datos siempre que se haya establecido la conexión con la base de datos
                print ("2")
                with open("restaurantes.json", "r") as f:
                    datos = json.load(f)
                
                if conexion:
                    conector.insertarDocumentosColeccion(datos, nombreColeccion)
                else:
                    print("Error en la conexión desde menú")
                

            case "3":
                # Mostrar los nombre de los restaurantes del código postal introducido siempre que se haya establecido la conexión con la base de datos
                print ("3")
                
                if conexion:
                    buscado = None
                    incorrecto = True
                    
                    while incorrecto:
                        buscado = input("Introduce el código postal: ")                
                            
                        if not buscado.isdigit():
                            print("Debe ser numérico")
                        elif len(buscado) != 5:
                            print("Código postal no válido (debe tener 5 dígitos)")
                        else:
                            incorrecto = False
                            
                    consulta = {"direccion.codigo_postal": {"$regex": f"^{buscado}","$options": "i"}}
                    
                    listaNombres= conector.consultarDocumentos(nombreColeccion, consulta)#Enviamos la consulta que queremos buscar
                    listaNombres = list(listaNombres)
                    #Recorremos la lista recuperada
                    
                    for e in listaNombres:
                        print(e["nombre"])
                        
                    print("Número de restaurantes encontrados:", len(listaNombres))
                
                else:
                    print("Error de conexión desde el menú")

            case "4":
                # Mostrar los restaurantes cuyo nombre o distrito empiecen por la cadena introducida siempre que se haya establecido la conexión con la base de datos
                print ("4")
                
                if conexion:
                    incorrecto = True
                    
                    while incorrecto:
                        buscado = input("Escribe el nombre: ")                
                            
                        if buscado.isdigit():
                            print("Debe ser una letra")
                        elif len(buscado) < 1:
                            print("Debe contener al menos una letra.")
                        else:
                            incorrecto = False
                            
                    consulta = {
                        "$or": [
                            {"nombre": {"$regex": f"^{buscado}", "$options": "i"}},
                            {"distrito": {"$regex": f"^{buscado}", "$options": "i"}}
                        ]
                    }
                    
                    listaRestaurantes= conector.consultarDocumentos(nombreColeccion, consulta)#Enviamos la consulta que queremos buscar
                    listaRestaurantes = list(listaRestaurantes)
                    
                    for e in listaRestaurantes:
                        print(e)
                    
                    print("Número de restaurantes encontrados:", len(listaRestaurantes))
                    
                else:
                    print("Error de conexión desde el menú.")

            case "5":
                # Mostrar el número de restaurante que hay por tipo de cocina siempre que se haya establecido la conexión con la base de datos
                print ("5")
                
                if conexion:
                    consulta = [{"$sortByCount":"$tipo_cocina"}]
                    resultado = conector.obtenerAgregacion(nombreColeccion,consulta)
                    
                    print("Restaurantes por tipo de cocina:")
                    
                    for r in resultado:
                        print(f"{r['_id']}: {r['count']}")
                else:
                    print("Error de conxión desde el menú.")

            case "6":
                # Mostrar los cinco resturantes con mejor calificación promedio siempre que se haya establecido la conexión con la base de datos
                print ("6")
                
                if conexion:
                    
                    consulta = [
                        {"$unwind": "$inspecciones"},
                        {
                            "$group": {
                                "_id": "$nombre",
                                "media": {"$avg": "$inspecciones.puntuacion"}
                            }
                        },
                        {"$sort": {"media": -1}},
                        {"$limit": 5}
                    ]
                    
                    resultado = conector.obtenerAgregacion(nombreColeccion, consulta)
                    
                    print("Los mejores 5 restaurantes:")
                    
                    for r in resultado:
                        print(f"{r["_id"]}: {round(r["media"],2)}")
                
                else:
                    print("Error de conexión desde el menú.")


            case "7":
                # Insertar una nota a un restaurante siempre que se haya establecido la conexión con la base de datos.
                # Hay insertar el ID del restaurante y comprobar que exista el mismo
                # Fecha en formato Unix timestamp (milisegundos) int(datetime.now(timezone.utc).timestamp() * 1000)  
                print ("7")
                
                if conexion:
                    
                    id_incorrecto = True
                    letras_incorrectas = True
                    puntuacion_invalido = True
                    letras_validas = ["A", "B", "C", "P", "Z"]
                    
                    while id_incorrecto: #Validación para ID
                        id = input("Introduce el id del restaurante: ")                
                            
                        if not id.isdigit():
                            print("Debe ser numérico")
                        else:
                            id_incorrecto = False
                            
                    restaurante = conector.encontrarDocumento(nombreColeccion,{"restaurante_id": id}) #Recupero el restaurante
                    if restaurante != 0: #Si es distinto de 0, es que existe restaurante y continuo con las validaciones
                                    
                        while letras_incorrectas: #Validación para la clasificación
                            letras = input("Introduce la clasificación (A, B, C, P o Z):") 
                                
                            if letras not in letras_validas:
                                print("La letra no es válida.")  
                            else:
                                letras_incorrectas = False 
                            
                        while puntuacion_invalido: # Validación para la puntuación
                            puntuacion = int(input("Introduce una puntuación entre 0 y 50: "))
                                
                            if 0 <= puntuacion <= 50:
                                puntuacion_invalido = False  
                            else: 
                                print("La puntuación no es válida")
                                    
                        #Una vez validado todo, creo la inspeccion
                        nueva_inspeccion = {
                            "fecha": {"$date": int(datetime.now().timestamp() * 1000)},
                            "calificacion": letras,
                            "puntuacion": puntuacion
                        }
                            
                        #Inserto la nueva inspeccion 
                        consulta = {"restaurante_id": id}

                        resultado = conector.insertarEnLista(
                            nombreColeccion,
                            consulta,
                            "inspecciones",
                            nueva_inspeccion
                        )
                            
                        #Comprobacion usando el contador de modificados
                        if resultado and resultado.modified_count > 0:
                            print("Inspección añadida correctamente")
                        else:
                            print("No se pudo añadir la inspección")
                                
                        restaurante = conector.encontrarDocumento(nombreColeccion,{"restaurante_id": id})
                            
                        print(f"Inspecciones del restaurante {restaurante["nombre"]}: {restaurante["inspecciones"]}")
                        
                    else:
                        print("No hay restaurante con ese id")
                            
                else:
                    print("Error de conexión desde el menú.")
                                
                    


            case "8":
                # Consulta voluntaria definida por el alumno siempre que se haya establecido la conexión con la base de datos.
                print ("8")
                
                if conexion:
                    
                    #Print
                    print("Los 3 distritos con más restaurantes: ")
                    consulta = [
                                {"$group": {"_id": "$distrito", "total": {"$sum": 1}}},
                                {"$sort": {"total": -1}},
                                {"$limit": 3}
                            ]
                    
                    podio = conector.obtenerAgregacion(nombreColeccion, consulta)
                    
                    for r in podio:
                        print(f"{r["_id"]}: {r["total"]}")
                        
                else:
                    print("Error de conexión desde el menú.")
               
            case "9":
                # Borrar todos los documentos siempre que se haya establecido la conexión con la base de datos.
                print ("9")
                if conexion:
                    conector.borrarDocumentosColeccion(nombreColeccion)
                else:
                    print("Error de conexion desde el menú.")


            case "10":
                # Cerrar conexión siempre que se haya establecido la misma anteriormente.
                print ("10")
                if conexion:
                    conector.cerrarConexion()
                    conexion=False
                else:
                    print("Error de conexión desde el menú")
               
            case _:
                 print("Opción no válida, intenta de nuevo.")
           


if __name__ == "__main__":
    main()    



