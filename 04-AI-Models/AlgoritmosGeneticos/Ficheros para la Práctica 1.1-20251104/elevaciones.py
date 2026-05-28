import matplotlib.pyplot as plt
import numpy as np
from cargar_datos import leer

from matplotlib import cm
from matplotlib.ticker import LinearLocator

# Convertir coordenada x en grados de longitud
def x_to_lon(x):
	return 3.8 + (10.25 + 3.8) * -x / 5000

# Convertir coordenada y en grados de latitud
def y_to_lat(y):
	return 43.8 - (43.8 - 35.7) * y / 4500

def obtener_mapa():
	
	# Cargamos el mapa y nos quedamos con la parte que nos interesa
	mapa = leer('altitud.asc')[8000:10000,0:1000]
	print('------------  Fichero Cargado -------------')
	print(mapa.shape)
	return mapa
	
def mostrar_mapa(mapa, punto_max=None, punto_min=None):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X = np.arange(mapa.shape[1])
    Y = np.arange(mapa.shape[0])
    X, Y = np.meshgrid(X, Y)

    surf = ax.plot_surface(X, Y, mapa, cmap=cm.terrain, linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 2000)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    if punto_max: #Punto máximo
        ax.scatter(punto_max[1], punto_max[0], mapa[punto_max[0], punto_max[1]],
                   s=150, c='red', marker='o', label='Máximo', edgecolors="black")

    if punto_min:  # Punto mínimo
        x = punto_min[1]
        y = punto_min[0]
        z_real = mapa[y, x]              # altitud real del punto
        z_top = z_real + 2000            # elevamos el punto para que sea visible

        # Pilar vertical para unir el punto real(suelo) con el punto elevado
        ax.plot([x, x], [y, y], [z_real, z_top], color='purple', linewidth=4)
        
        # Punto en la cima del pilar
        ax.scatter(x, y, z_top, s=150, c='purple', marker='o', label='Mínimo', edgecolors="black")


    plt.legend()
    plt.show()


