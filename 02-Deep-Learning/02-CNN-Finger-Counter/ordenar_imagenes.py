import os
import shutil
import re

carpeta_origen = r"C:\Users\David\Desktop\IA y BigData\PIA\Tema 10\dedos"
carpeta_base = r"C:\Users\David\Desktop\IA y BigData\PIA\Tema 10"

for i in range(0, 6):
    carpeta_destino = os.path.join(carpeta_base, str(i))
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

for archivo in os.listdir(carpeta_origen):
    if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        match = re.search(r'_(\d)([LR])\.', archivo)
        if match:
            numero = match.group(1)
            origen = os.path.join(carpeta_origen, archivo)
            destino = os.path.join(carpeta_base, numero, archivo)
            shutil.move(origen, destino)
            print(f"Moved {archivo} -> carpeta {numero}")