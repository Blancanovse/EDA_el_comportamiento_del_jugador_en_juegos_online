import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#Funciones vistas en el bootcamp (bootcampviztools.py) con pequeñas modificaciones en algunas de ellas:

# ----------------------------------------------------------------------

#Funcion para calcular la cardinalidad y clasificar las varibales según su tipo:

def clasificador_variables(df,umbral_categoria, umbral_continua):
    ''' Devuelve un dataframe con la cardinalidad de los valores de cada columna, su porcentaje de cardinalidad
        y el tipo de clasficiación de cada variable según los parámetros introducidos.

        Atención: está adaptada a las necesidades de este EDA.
        
        Argumentos:
        df : pandas.Dataframe del que queremos obtener la cardinalidad y clasificación de variables
        umbral_categorica: umbral establecido para determinar el tipo de las variables categóricas.
        umbral_continua: umbral establecido para determinar el tipo de las varibales numéricas. 
    '''
    
    df = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, df.dtypes]) # Cardinaliad, porcentaje y tipo de datos.
    df = df.T # Transponer para obtener los datos en filas
    df = df.rename(columns = {0: "Cardinalidad", 
                              1: "%_Cardinalidad", 
                              2: "Tipo"}) # Renombra las columnas


    # Se aplican los filtros para la clasificación de las variables:
    df["Tipo_Variable"] = "Categórica"  #Por defecto serán categóricas ya que muchas de ellas lo son.
    df.loc[df["Cardinalidad"] == 2, "Tipo_Variable"] = "Binaria"
    df.loc[df["Cardinalidad"] >= umbral_categoria, "Tipo_Variable"] = "Numérica discreta"
    df.loc[df["%_Cardinalidad"] >= umbral_continua, "Tipo_Variable"] = "Numérica continua"

    return df

#-----------------------------------------------------
#Obtener el IQR:

def get_IQR(df, col):
    '''
        Devuelve el rango intercuantílico de una variable.

        Args:
        df: Pandas Dataframe
        col: columna (variable) del dataframe 
    '''
    return df[col].quantile(0.75) - df[col].quantile(0.25)

#-----------------------------------------------------

#Ver el CV:

def variabilidad(df):
    '''
        Devuelve el coeficiente de variación (CV) en porcentajes.
    '''
    df_var = df.describe().loc[["std", "mean"]].T
    df_var["CV"] = df_var["std"]/ df_var["mean"]
    return df_var

#------------------------------------------------------

# Graficar: 

def pinta_distribucion_categoricas(df, columnas_categoricas, relativa=False, mostrar_valores=False):
    ''' Devuelve la distribución de las variables categóricas en gráficas.

        Args:
        df: Pandas DataFrame
        columnas_categoricas: variables categoricas
        relativa : por defecto false. Para que sea absoluta =True
        mostrar_valores: por defecto false
    '''
    num_columnas = len(columnas_categoricas)
    num_filas = (num_columnas // 2) + (num_columnas % 2)

    fig, axes = plt.subplots(num_filas, 2, figsize=(15, 5 * num_filas))
    axes = axes.flatten() 

    for i, col in enumerate(columnas_categoricas):
        ax = axes[i]
        if relativa:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='cool', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia Relativa')
        else:
            serie = df[col].value_counts()
            sns.barplot(x=serie.index, y=serie, ax=ax, palette='cool', hue = serie.index, legend = False)
            ax.set_ylabel('Frecuencia')

        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)

        if mostrar_valores:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_filas * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


#--------------------------------------------------------

def plot_multiple_boxplots(df, columns, dim_matriz_visual = 2):
    ''' 
        Devuelve una gráfica con el conjunto de diagrama de cajas de cada variable numérica.

        Args:
        df: Pandas Dataframe
        columns : columna (variable) del dataframe
        dim_matriz_visual : por defecto 2 columnas 
    '''
    num_cols = len(columns)
    num_rows = num_cols // dim_matriz_visual + num_cols % dim_matriz_visual
    fig, axes = plt.subplots(num_rows, dim_matriz_visual, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.boxplot(data=df, x=column, ax=axes[i], color="skyblue")
            axes[i].set_title(column)

    # Ocultar ejes vacíos
    for j in range(i+1, num_rows * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

# -----------------------------------------------------------------

def plot_histo_den(df, columns):
    '''
        Muestra el conjunto de histogramas y densidad en una figura.

        Args:
        df: Pandas Dataframe
        columns: columnas(variables) numéricas. 
    '''
    num_cols = len(columns)
    num_rows = num_cols // 2 + num_cols % 2
    fig, axes = plt.subplots(num_rows, 2, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.histplot(df[column], kde=True, ax=axes[i], color="orange", bins=20)
            axes[i].set_title(f'Histograma y KDE de {column}')

    # Ocultar ejes vacíos
    for j in range(i + 1, num_rows * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


# ----------------------------------------------------

def plot_combined_graphs(df, columns, whisker_width=1.5):
    ''' Devuelve una figura que combina diagramas de cajas e histogramas por cada variable.
        
        Args:
        df: Pandas Dataframe
        columns: columnas(variables) numéricas.
        whisker_width: por defecto 1.5
    '''
    num_cols = len(columns)
    if num_cols:
        
        fig, axes = plt.subplots(num_cols, 2, figsize=(12, 5 * num_cols))
        print(axes.shape)

        for i, column in enumerate(columns):
            if df[column].dtype in ['int64', 'float64']:
                # Histograma y KDE
                sns.histplot(df[column], kde=True, ax=axes[i,0] if num_cols > 1 else axes[0], color="orange", bins=20)
                if num_cols > 1:
                    axes[i,0].set_title(f'Histograma y KDE de {column}')
                else:
                    axes[0].set_title(f'Histograma y KDE de {column}')

                # Boxplot
                sns.boxplot(x=df[column], ax=axes[i,1] if num_cols > 1 else axes[1], whis=whisker_width, color="skyblue")
                if num_cols > 1:
                    axes[i,1].set_title(f'Boxplot de {column}')
                else:
                    axes[1].set_title(f'Boxplot de {column}')

        plt.tight_layout()
        plt.show()

# ------------------------------------------------------------------------------------

def plot_categorical_relationship_fin(df, cat_col1, cat_col2, relative_freq=False, show_values=False, size_group = 5):
    ''' 
        Pinta relación entre variables categóricas
    
    '''
    # Prepara los datos
    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name='count')
    total_counts = df[cat_col1].value_counts()
    
    # Convierte a frecuencias relativas si se solicita
    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis=1)

    # Si hay más de size_group categorías en cat_col1, las divide en grupos de size_group
    unique_categories = df[cat_col1].unique()
    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=data_subset, order=categories_subset)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {cat_col1} y {cat_col2} - Grupo {i + 1}')
            plt.xlabel(cat_col1)
            plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de size_group categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=count_data)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {cat_col1} y {cat_col2}')
        plt.xlabel(cat_col1)
        plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()


# -----------------------------------------------

def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values=False, measure='mean'):
    '''  
        Pinta relación entre variables categóricas
    '''
    # Calcula la medida de tendencia central (mean o median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        # Por defecto, usa la media
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Ordena los valores
    grouped_data = grouped_data.sort_values(ascending=False)

    # Si hay más de 5 categorías, las divide en grupos de 5
    if grouped_data.shape[0] > 5:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / 5))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * 5:(i + 1) * 5]
            data_subset = grouped_data.loc[categories_subset]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=data_subset.index, y=data_subset.values)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {categorical_col} y {numerical_col} - Grupo {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de 5 categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=grouped_data.index, y=grouped_data.values)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {categorical_col} y {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()


# ---------------------------------------------

def plot_grouped_histograms(df, cat_col, num_col, group_size, bins = "auto"):
    unique_cats = df[cat_col].unique()
    num_cats = len(unique_cats)

    for i in range(0, num_cats, group_size):
        subset_cats = unique_cats[i:i+group_size]
        subset_df = df[df[cat_col].isin(subset_cats)]
        
        plt.figure(figsize=(10, 6))
        for cat in subset_cats:
            sns.histplot(subset_df[subset_df[cat_col] == cat][num_col], kde=True, label=str(cat), bins = bins)
        
        plt.title(f'Histograms of {num_col} for {cat_col} (Group {i//group_size + 1})')
        plt.xlabel(num_col)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

# --------------------------------------------

def grafico_dispersion_con_correlacion(df, columna_x, columna_y, tamano_puntos=50, mostrar_correlacion=False):
    """
    Crea un diagrama de dispersión entre dos columnas y opcionalmente muestra la correlación.

    Args:
    df (pandas.DataFrame): DataFrame que contiene los datos.
    columna_x (str): Nombre de la columna para el eje X.
    columna_y (str): Nombre de la columna para el eje Y.
    tamano_puntos (int, opcional): Tamaño de los puntos en el gráfico. Por defecto es 50.
    mostrar_correlacion (bool, opcional): Si es True, muestra la correlación en el gráfico. Por defecto es False.
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columna_x, y=columna_y, s=tamano_puntos)

    if mostrar_correlacion:
        correlacion = df[[columna_x, columna_y]].corr().iloc[0, 1]
        plt.title(f'Diagrama de Dispersión con Correlación: {correlacion:.2f}')
    else:
        plt.title('Diagrama de Dispersión')

    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.grid(True)
    plt.show()

# ----------------------------------------------

def bubble_plot(df, col_x, col_y, col_size, scale = 1000):
    """
    Crea un scatter plot usando dos columnas para los ejes X e Y,
    y una tercera columna para determinar el tamaño de los puntos.

    Args:
    df (pd.DataFrame): DataFrame de pandas.
    col_x (str): Nombre de la columna para el eje X.
    col_y (str): Nombre de la columna para el eje Y.
    col_size (str): Nombre de la columna para determinar el tamaño de los puntos.
    """

    # Asegúrate de que los valores de tamaño sean positivos
    sizes = (df[col_size] - df[col_size].min() + 1)/scale

    plt.scatter(df[col_x], df[col_y], s=sizes)
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.title(f'Burbujas de {col_x} vs {col_y} con Tamaño basado en {col_size}')
    plt.show()

# ---------------------------------------------

def plot_grouped_boxplots(df, cat_col, num_col):
    unique_cats = df[cat_col].unique()
    num_cats = len(unique_cats)
    group_size = 5

    for i in range(0, num_cats, group_size):
        subset_cats = unique_cats[i:i+group_size]
        subset_df = df[df[cat_col].isin(subset_cats)]
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=cat_col, y=num_col, data=subset_df)
        plt.title(f'Boxplots of {num_col} for {cat_col} (Group {i//group_size + 1})')
        plt.xticks(rotation=45)
        plt.show()


# ---------------------------------------------

def scatter_plot_with_controls(df, x_col, y_col,color_col = None, size_col = "", scale=1, legend = True):

    fig, ax = plt.subplots(figsize = (20,10)) # Cuando creas 1 sólo gráfico no hace falta poner 1,1
    # Creamos el scatter en función de los argumentos de entrada
    sizes = (100,1000)
    if type(size_col) == str: # So 
        if size_col != "": # Si el argumento size es un str consideramos que es una de las columnas del dataframe
            if color_col: # Ahora comprobamos que realmente haya columna de color
                scatter = sns.scatterplot(x = x_col, y = y_col, size = df[size_col] * scale, data = df, hue = color_col, 
                                          alpha = 0.5, palette = "viridis", ax = ax, sizes = sizes)
            else: # No hay columna de color, así que no lo pasamos como argumento y dejamos que lo escoja el método
                scatter = sns.scatterplot(x = x_col, y = y_col, size = df[size_col] * scale, data = df, 
                                          alpha = 0.5, palette = "viridis", ax = ax, sizes = sizes)
        elif color_col: # Si hay categoria de color y además datos de tamaño que no son una columna
            scatter = sns.scatterplot(x = x_col, y = y_col, data = df, hue = color_col, alpha=0.5, palette='viridis', ax = ax, sizes = sizes) # Ojo no aplicamos la escala
    else:
        scatter = sns.scatterplot(x = x_col, y = y_col, size = size_col, data = df, alpha=0.5, palette='viridis', ax = ax, sizes = sizes) # Ojo no aplicamos la escala, ni el color
    # Labels

    if legend:
        ax.legend(ncol = 2, loc="upper right", frameon = False, labelspacing = 2)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    return ax
