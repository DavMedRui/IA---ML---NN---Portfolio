from whoosh import index
from whoosh.qparser import QueryParser


def buscar(consulta: str, campo: str = "cuerpo"):
    indice = index.open_dir("indice_buscador")
    
    with indice.searcher() as searcher:
        query_parser = QueryParser(campo, indice.schema)
        query = query_parser.parse(consulta)
        resultados = searcher.search(query)
        
        print(f"\nResultados para '{consulta}' en campo '{campo}':")
        print("-" * 50)
        
        if len(resultados) == 0:
            print("No se encontraron resultados.")
        else:
            for resultado in resultados:
                print(f"Titulo: {resultado['titulo']}")
                print(f"URL: {resultado['url']}")
                print(f"Resumen: {resultado['resumen'][:200]}...")
                print("-" * 50)


if __name__ == "__main__":
    print("Buscador de documentos PDF")
    print("=" * 50)
    
    seguir = True
    while seguir:
        consulta = input("\nIntroduce tu busqueda (o 'salir' para terminar): ")
        if consulta.lower() == "salir":
            seguir = False
        else:
            campo = input("Campo donde buscar (cuerpo/titulo/resumen) [por defecto cuerpo]: ")
            if campo == "":
                campo = "cuerpo"
            buscar(consulta, campo)
