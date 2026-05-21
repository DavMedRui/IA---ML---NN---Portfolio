# %% [markdown]
# # PRÁCTICA: ANÁLISIS EXPLORATORIO DE DATOS
# Programación de IA

# %% [markdown]
# En esta practica, dispondremos del dataset AB_NYC_2019 que describe la actividad de los alojamientos suscritos a la plataforma Airbnb en la ciudad de New York en el año 2019. 
# La práctica consiste en realizar un análisis exploratorio de datos completos y dejar los datos "limpios" para su uso.

# %%
# Importación de librerías y lectura del dataset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar el dataset
df = pd.read_csv('AB_NYC_2019.csv') #Quitamos la columna id que se añade por defecto al cargar el dataset
# Mostrar las primeras filas del dataset
df.head()

# %% [markdown]
# # Grado de fiabilidad. Regla del 10
# Comprobaremos que se cumpla la Regla del 10: nºfilas >= nºcolumnas*10

# %%
#Numero de columnas
columnas = df.drop(["id", "host_id"], axis=1).columns
print("Número de columnas:", len(columnas))

#Número de filas
filas = len(df)
print("Número de filas:", filas)

#Regla del 10
print("Límite para cumplir la regla del 10:", len(columnas)*10)
if filas > len(columnas)*10:
    print("El dataset cumple con la regla del 10.")
else:
    print("El dataset no cumple con la regla del 10.")

# %% [markdown]
# # Análisis Descriptivo

# %% [markdown]
# Información sobre el dataset

# %%
#Información del dataset, cuantos valores nulos hay, tipo de datos, etc.
df.info()

# %%
# Lista de columnas
df.columns

# %%
#Datos estadísticos
df.describe()

# %% [markdown]
# Visualizaciones gráficas para el dataset
# A continuación se muestran algunos ejemplos de visualizaciones útiles para el análisis exploratorio de este dataset:
# 
# 1. Histograma de precios
# 2. Gráfico de barras de alojamientos por barrio
# 3. Mapa de dispersión geográfica (latitud vs longitud)
# 4. Gráfico de barras por tipo de habitación
# 
# Se incluye el código para cada visualización.

# %%
# 1. Histograma de precios
plt.figure(figsize=(8,5))
df['price'].hist(bins=50, color='skyblue', edgecolor='black')
plt.title('Distribución de precios de los alojamientos')
plt.xlabel('Precio por noche (USD)')
plt.ylabel('Frecuencia')
plt.xlim(0, 500)
plt.show()

# %%
# 2. Gráfico de barras de alojamientos por barrio
plt.figure(figsize=(8,5))
df['neighbourhood_group'].value_counts().plot(kind='bar', color='coral', edgecolor='black')
plt.title('Número de alojamientos por barrio')
plt.xlabel('Barrio')
plt.ylabel('Cantidad de alojamientos')
plt.show()

# %%
# 3. Mapa de dispersión geográfica de alojamientos
plt.figure(figsize=(8,6))
plt.scatter(df['longitude'], df['latitude'], c=df['neighbourhood_group'].astype('category').cat.codes, cmap='tab10', alpha=0.4, s=10)
plt.title('Distribución geográfica de los alojamientos')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.show()

# %%
# 5. Gráfico de barras por tipo de habitación
plt.figure(figsize=(8,5))
df['room_type'].value_counts().plot(kind='bar', color='mediumseagreen', edgecolor='black')
plt.title('Número de alojamientos por tipo de habitación')
plt.xlabel('Tipo de habitación')
plt.ylabel('Cantidad de alojamientos')
plt.show()

# %% [markdown]
# ## Tipos de variables

# %%
df.head(3)

# %% [markdown]
# Tipos de cada columna. Usaremos la visualización de los 3 primeros apartamentos para comprobar que cada columna corresponde con el tipo de dato.

# %%
# Tipos de cada columna
df.dtypes

# %% [markdown]
# Observamos que la columna "price" es de tipo object (string) pero en el dataframe son enteros, por tanto conviene realizar la transformación.
# 
# Ocurre lo mismo con la columna "week_price" y "swimming pool".

# %%
# Tranformamos la columna "price" y "week_price" a tipo numérico
df["price"] = pd.to_numeric(df["price"], errors='coerce') #Usamos coerce para convertir los valores no válidos a NaN
df["week_price"] = pd.to_numeric(df["week_price"], errors='coerce')
df["swimming pool"] = pd.to_numeric(df["swimming pool"], errors='coerce')

# %%
#Comprobamos de nuevo los tipos de cada columna
df.dtypes

# %% [markdown]
# Tratamiento de datos ausentes

# %%
# Comprobaremos los valores ausentes de todas las columnas
print("Valores nulos por columna:")
print(df.isnull().sum())

#Valores nulos por fila
print("\nFilas por valores nulos:")
print(df.isnull().sum(axis=1).value_counts())

# %% [markdown]
# A partir de estos datos tomaremos distintas soluciones para distintas columnas:
# 
# 1. Columnas name, host_name, price y week_price: eliminaremos las FILAS, ya que es un número bastante bajo en comparación a la cantidad de filas totales que hay en el dataframe.
# 
# 
# 2. Columnas swimming pool, last_review y reviews_per_month: sustituiremos los valores NaN por otros valores válidos.
# 

# %% [markdown]
# # 1. Eliminación de filas

# %%
#Eliminamos las filas con algún valor nulo de las columnas price, week_price, name y host_namen
df = df.dropna(subset=['price', 'week_price', 'name', 'host_name'])
#Comprobamos de nuevo los valores nulos por columna
print("\nValores nulos por columna después de eliminar filas con valores nulos:")
print(df.isnull().sum())

# %% [markdown]
# # 2. Swimming Pool, last_review y reviews_per_month

# %% [markdown]
# # Swimming Pool

# %% [markdown]
# A continuación, comprobaremos los valores existentes en la columna "swimming pool".

# %%
#Mostramos valores
print("Valores válidos en 'swimming pool': ", df["swimming pool"].value_counts())

#Mostrar valores Nan en "swimming pool"
print("Valores nulos en 'swimming pool': ", df["swimming pool"].isna().sum())

# %% [markdown]
# Como podemos observar, obtenemos 35744 valores 0, lo cual quiere decir que el apartamento no cuenta con piscina.
# Por otro lado, 9770 apartamentos que sí las tienen.
# 
# Este caso resulta muy abierto a interpretaciones, ya que contar con 3220 valores NaN no puede "no significar nada". 
# 
# ¿Qué significa el NaN en esta columna? ¿Podría significar que el apartamento NO cuenta con piscina? Desde mi punto de vista, el caso más lógico sería este último: NaN no es un dato desconocido, sino que muy probablemente signifique que el apartamento no tiene piscina y es por ello mi decisión de rellenar los valores NaN con 0

# %%
# Relleno los valores NaN de "swimming pool" por 0
df["swimming pool"] = df["swimming pool"].fillna(0)

# %%
#Comprobamos
print("Valores nulos en 'swimming pool' después de rellenar con 0: ", df["swimming pool"].isna().sum())
print("Valores válidos en 'swimming pool' después de rellenar con 0: ", df["swimming pool"].value_counts())

# %% [markdown]
# # Reviews_per_month

# %% [markdown]
# Aquí podemos decir que existe un caso parecido. 
# 
# En una variable que recoge la cantidad de reviews por mes, si existe valores NaN, ¿es porque no hay reviews o porque no se pueden calcular?
# 
# En mi caso, los valores NaN que aparecen en esta columna se pueden interpretar como que no se ha registrado ninguna review en el mes, así que pueden rellenarse como valor 0.

# %%
# Vemos cuantos valores nulos hay en "reviews_per_month"
print("Valores no validos en la columna 'reviews_per_month': ", df["reviews_per_month"].isna().sum())

# %%
# Rellenamos valores nulos como 0
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

# %%
#Comprobamos de nuevo los valores nulos por columna
print("\nValores nulos por columna después de rellenar 'reviews_per_month' con 0:", df["reviews_per_month"].isna().sum())

# %% [markdown]
# # last_review

# %% [markdown]
# Para esta columna, hemos decidido eliminar esta columna, puesto que tenemos otras dos que nos aportan información relacionada ("reviews_per_month" y "numbers_of_review") y así evitamos imputar fechas.

# %%
#Eliminamos la columna last_review
df = df.drop("last_review", axis = 1)
df

# %% [markdown]
# # id y host_id
# 
# Borraremos estas dos columnas, puesto que son id's que se han asignado y no aportan ningún valor

# %%
df.drop(columns=["id", "host_id"], axis=1, inplace=True)

# %% [markdown]
# A continuación, revisaremos que todos los valores sean correctos.

# %%
# Revisión de valores anómalos y tipos de datos
print('--- Revisión de valores "?", "NA", "None", "null" o vacíos por columna ---')
for col in df.columns:
    count_q = (df[col] == '?').sum() if df[col].dtype == 'object' else 0
    count_na = (df[col] == np.nan).sum() if df[col].dtype == 'object' else 0
    count_none = (df[col] == 'None').sum() if df[col].dtype == 'object' else 0
    count_null = (df[col] == 'null').sum() if df[col].dtype == 'object' else 0
    count_empty = (df[col] == '').sum() if df[col].dtype == 'object' else 0
    if any([count_q, count_na, count_none, count_null, count_empty]):
        print(f'{col}: ?={count_q}, NA={count_na}, None={count_none}, null={count_null}, vacío={count_empty}')

print('\n--- Revisión de valores NaN por columna ---')
print(df.isnull().sum())

print('\n--- Tipos de datos de cada columna ---')
print(df.dtypes)

# %%
print(df.dtypes)
df.head(5)

# %% [markdown]
# # Datos Atípicos
# 
# En este apartado, trateremos los datos atípicos como valores duplicados y outliers

# %%
#Visualizamos filas de datos duplicados
if any(df.duplicated()):
    print("existen filas duplicadas")
else: 
    print("No existen filas duplicadas")

# %% [markdown]
# Podemos comprobar que no existen filas duplicadas.
# 
# A continuación, usaremos boxplot para buscar outliers. Para ello, lo buscaremos en las columnas numéricas

# %%
# Miramos para seleccionar
df.dtypes

# %%
#Columnas numéricas. En ellas excluiremos latitud y longitud, puesto que la información que aportan son sobre localizaciones
numericas = ["price", "minimum_nights", "number_of_reviews", "reviews_per_month", "calculated_host_listings_count", "availability_365", "week_price"]

#Vamos a representar los boxplots
for c in numericas:
    bp = plt.boxplot(df[c])
    
    plt.title(f"Boxplot de {c}")
    plt.show()




# %% [markdown]
# Como podemos observar, en todas las columnas seleccionadas existen gran número de outliers salvo en availability_365. Será excluida de la lista y los demás elementos serán tratados, recortando los outliers a valores máximos o minimos según convenga.

# %%
#Columnas numéricas. En ellas excluiremos latitud y longitud, puesto que la información que aportan son sobre localizaciones
numericas = ["price", "minimum_nights", "number_of_reviews", "reviews_per_month", "calculated_host_listings_count", "week_price"]

#Vamos a representar los boxplots
for c in numericas:
    
    plt.figure()
    bp = plt.boxplot(df[c])
    
    # Antes
    outliers_ant = bp["fliers"][0].get_ydata()
    valor_min = bp["caps"][0].get_ydata()[0]
    valor_max = bp["caps"][1].get_ydata()[0]
    
    # Aplicamos filtro 
    df.loc[df[c] > valor_max, c] = valor_max
    df.loc[df[c] < valor_min, c] = valor_min
    plt.title(f"Boxplot de {c} antes")
    
    # Después
    plt.figure()
    bp = plt.boxplot(df[c])
    outliers_desp = bp["fliers"][0].get_ydata()
    
    print(f"{c} -> Antes: {len(outliers_ant)} | Después: {len(outliers_desp)}")
    
    plt.title(f"Boxplot de {c} después")
    plt.show()





# %% [markdown]
# # Correlación
# 
# Después de haber tratado los datos atípicos, haremos un estudio de la correlación. Como la correlación solo se puede calcular de atributos numéricos, solo lo haremos con las columnas que sean de este tipo.

# %%
import seaborn as sns

#Creamos un df con solo los tipos numericos
correlacion = pd.DataFrame()
for c in df.columns:
    if df[c].dtype !="object":
        correlacion[c] = df[c]

#Correlación
matriz = correlacion.corr()
sns.heatmap(matriz, cmap="coolwarm", annot=True)
plt.show()

# %% [markdown]
# Podemos observar que week_price y price aportan la misma información, por tanto procedemos a eliminar una de las dos, por ejemplo week_price

# %%
#Eliminamos week_price
df = df.drop("week_price", axis=1)
df


