"""
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

def FARGO3DVisualize(data_path, file_range, output_file, fps, file_pattern):
    
    '''
    FARGO3DVisualize es una función que utiliza los datos de simulaciones generadas con el software de FARGO3D para
    obtener visualizaciones de la simulación realizada.
   
    Argumentos de la función:
    data_path (string): Path del directorio donde tengamos los datos de simulación.
    file_range (tupla): Rango de cuántos outputs queremos leer de los que ha generado la simulación.
    output_file (string): Este es el nombre del archivo que crearemos. Está en formato GIF.
    fps (int): Los frames por segundo del gif generado. Predeterminadamente utiliza 15.
    file_pattern (string): El código lee los outputs siguiendo un patrón en el nombre, para de esta forma detectar cuál de
    todos los archivos le será de utilidad. Acá se coloca el patrón del nombre del archivo de la simulación que
    queremos utilizar.
   
    Output:
    El output de la función es una visualización en formato GIF de la simulación realizada por FARGO3D.
    
    #Ejemplo de uso
    path = '/content/drive/MyDrive/Fargo3D/outputs/fargo' #Path
    file_range = (1, 49)  # El rango de los datos
    output_file = '/content/drive/MyDrive/Fargo3D/outputs/gasvy1.gif' #Dirección de guardado y nombre del archivo generado
    fps = 20 # fps de la animación
    file_pattern = "gasvy"  # Variable que queremos graficar
    
    
    #Llamamos a la funcion con los fps que queramos:
    FARGO3DVisualize(path, file_range, output_file, fps, file_pattern)
    '''

    #Coordenadas polares
    phi = np.loadtxt(data_path + "/domain_x.dat")[:-1] #Usamos domain_x.dat para definir el ángulo
    r = np.loadtxt(data_path + "/domain_y.dat")[3:-4] #Usamos domain_y.dat para definir el r
    #[:-1] y [3:-4] es una notación que utiliza FARGO3D

    #Definimos variables con el largo del ángulo phi y el radio r que utilizaremos más adelante.
    nphi = len(phi)
    nr = len(r)

    pattern = file_pattern+"{}.dat" #Generalizamos el código para que pueda leer cualquier archivo que termine en .dat
    
    file_numbers = [] #Variable que guarda la cantidad de archivos que tenemos en el path según nuestro file_pattern
    #Recorremos rango de valores que establecimos en el argumento de la función
    for i in range(file_range[0], file_range[1]+1):
        file_path = data_path + "/" + pattern.format(i)
        if os.path.isfile(file_path):
            file_numbers.append(i)

    densidades = []

    for i in file_numbers:
        file_path = data_path + "/" + pattern.format(i)
        densidades.append(np.fromfile(file_path).reshape(nr, nphi))

    print("Total frames:", len(densidades))

    fig = plt.figure()

    # Si no es especifican los fps se vuelve al default de 15
    if fps is not None:
        writer = PillowWriter(fps=int(fps))
    else:
        writer = PillowWriter(fps=15)

    try:
        with writer.saving(fig, output_file, 100):
            for i in range(len(densidades)):
                plt.imshow(densidades[i])
                plt.axis('off')  # ocultar los ejes, esto se puede cambiar si queremos.
                writer.grab_frame()

        if len(writer._frames) == 0:
            raise ValueError("No frames were added to the animation. Please check your data and file pattern.")

    #Excepción en caso de que no hay frames para crear GIF
    except IndexError:
        print("Error occurred while generating GIF. Generating PNG instead.")
        output_file = os.path.splitext(output_file)[0] + ".png"
        if len(densidades) > 0:
            plt.imshow(densidades[0])
            plt.axis('off')
            plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
        else:
            print("No frames available for PNG generation.")
            
            