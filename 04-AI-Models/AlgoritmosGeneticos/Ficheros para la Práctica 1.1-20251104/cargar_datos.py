import numpy as np

def leer(nombrefichero: str) :
	with open(nombrefichero) as fichero:
		linea = fichero.readline()
		ncols = int(linea.split()[1])
		linea = fichero.readline()
		nrows = int(linea.split()[1])
		array = np.ndarray((ncols, nrows), float)
		print(array.shape)
		fichero.readline()
		fichero.readline()
		fichero.readline()
		nodata = int(fichero.readline().split()[1])
		print('nodata:', nodata)
		for row in range(nrows):
			linea = fichero.readline()
			col = 0
			values = linea.split(' ')
			for col in range(ncols):
				value = float(values[col].replace(',', '.'))
				array[col][row] = value
				if value < -100:
					array[col][row] = -2000
	return array

