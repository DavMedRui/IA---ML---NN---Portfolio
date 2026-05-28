import os
import glob

from pdfquery import PDFQuery
from whoosh import index
from whoosh.fields import Schema, TEXT


def extraer_texto_pdf(pdf_path: str) -> str:
    pdf = PDFQuery(pdf_path)
    pdf.load()
    text_elements = pdf.pq('LTTextLineHorizontal, LTTextBoxHorizontal, LTChar')
    text = [t.text for t in text_elements]
    return '\n'.join(text)


def crear_indice():
    esquema = Schema(
        url=TEXT(stored=True),
        titulo=TEXT(stored=True),
        cuerpo=TEXT(stored=True),
        resumen=TEXT(stored=True)
    )
    
    if not os.path.exists("indice_buscador"):
        os.mkdir("indice_buscador")
    
    index.create_in("indice_buscador", esquema)
    return index.open_dir("indice_buscador")


def indexar_pdfs(carpeta: str, indice):
    writer = indice.writer()
    
    pdfs = glob.glob(os.path.join(carpeta, "*.pdf"))
    
    for pdf_path in pdfs:
        url = pdf_path
        titulo = os.path.basename(pdf_path)
        contenido = extraer_texto_pdf(pdf_path)
        
        resumen = contenido[:1000]
        cuerpo = contenido[:1000]
        
        writer.add_document(
            url=url,
            titulo=titulo,
            cuerpo=cuerpo,
            resumen=resumen
        )
        print(f"Indexado: {titulo}")
    
    writer.commit()


if __name__ == "__main__":
    carpeta = "contenido"
    
    indice = crear_indice()
    indexar_pdfs(carpeta, indice)
    
    print("\nIndexacion completada.")
