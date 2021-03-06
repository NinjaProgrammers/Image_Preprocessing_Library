
# Preprocesamiento de Imágenes



## dermoscopy_preprocessing

El objetivo de esta biblioteca es el preprocesamiento de imágenes de dermatoscopio. Se brindan métodos
para la mejora de contraste, bordes e iluminación. También se incluyen métodos para la eliminación
de artefactos. Su uso es exclusivo para imágenes de dermatoscopio, los resultados en otro tipo
de imágenes no se han comprobado.

## Autores

[Claudia Olavarrieta Martínez](https://github.com/ClaudiaOM)

[Marcos Adrián Valdivié Rodríguez](https://github.com/mavaldivie)

[Luis Enrique Dalmau Coopat](https://github.com/lukedalmau)

## Instalación

Como aún está en progreso el desarrollo de la biblioteca solo se ofrece una version de prueba que
puede ser descargada desde:


[https://github.com/ClaudiaOM/Image_Preprocessing_Library/tree/master/dist](https://github.com/ClaudiaOM/Image_Preprocessing_Library/tree/master/dist)

El código fuente se encuentra en 


[https://github.com/ClaudiaOM/Image_Preprocessing_Library](https://github.com/ClaudiaOM/Image_Preprocessing_Library)


Requiere como dependencias _opencv_ y _numpy_

## Uso

La biblioteca está dividida en submódulos orientados a la mejora de aspectos específicos que afectan 
la calidad de una imagen dermatoscópica. 

### Eliminación de artefactos

Una de las principales dificultades del procesamiento de imágenes dermatoscópicas es la presencia
de artefactos (cabellos, reglas de medición, burbujas de aire, etc) que imposibilitan el análisis de la zona de la piel lesionada. Las funciones de este 
módulo están enfocadas en remover los artefactos utilizando distintas técnicas:

- Eliminación de artefactos usando clausura morfológica (morphological_closure_artifact_removal)
    > El algoritmo consiste en aplicar primeramente a la imagen un filtro de media para eliminar
    ruido y luego aplicar clausura sobre la imagen. Esto se realiza por cada uno de los canales de RGB.
                                                                                                                                                                                                    
    >    **:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB 
    > 
    >    **:param** kernel: Núcleo a utilizar en la clausura
    >
    >    **:param** blur: True o False: Indica si un filtro de media debe ser aplicado antes de la operación de clausura morfológica
    >
    >    **:return:** Imagen resultante de mezclar cada canal RGB después de aplicar la clausura 

- Dull Razor (dull_razor_artifact_removal)
    > Se aplica una dilatación y luego una erosión, luego se calcula la diferencia entre la imagen obtenida y la original.
      Se vuelve a realizar una clausura sobre esta diferencia y luego se crea una imagen binaria que será la máscara
      de los artefactos. Luego se reemplazan los píxeles de la imagen original que pertenezcan a la máscara.

    >   **:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB 
    >
    >   **:param** kernel: Núcleo a utilizar en las operaciones morfológicas Blackhat
    >
    >   **:return:** Imagen resultante de mezclar cada canal RGB después de aplicar dull razor 
    >
- Bothat (bothat_artifact_removal)
    > Se aplica filro para eliminar ruido seguido de fitro de mejora de bordes. Luego se aplica una 
      la transformación morfológica bottomhat. Luego se aplica una mejora del contraste y se obtiene 
      una imagen binaria que será la máscara
      de los artefactos. Luego se reemplazan los píxeles de la imagen original que pertenezcan a la máscara.

    >   **:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB 
    >
    >   **:param** kernel: Núcleo a utilizar en las operaciones morfologicas Blackhat
    >
    >   **:return:** Imagen resultante de mezclar cada canal RGB despues de aplicar bothat
    >
- Laplaciano de Gauss (laplasian_of_gaussian)
    >  El método Laplaciano de Gauss se aplica a cada canal. Se realiza una dilatacion seguida por una 
       erosion y luego se mezclan los resultados de cada canal.
    >
    >   **:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB
    >
    >   **:return:** Imagen resultante de mezclar cada canal RGB despues de aplicar Laplacian of Gaussian
- Limpieza de artefactos restantes (clean_remaining_artifacts)
    > **Método aún en desarrollo. Use con cautela.**
    >   Elimina artefactos restantes utilizando operaciones morfológicas
    >
    >   **:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB
    >
    >   **:return:** Imagen

Ejemplo de uso:

```python
from dermoscopy_preprocessing import artifacts_removal
from dermoscopy_preprocessing.utils import CIRCLE_KERNEL_5X5 as cc5


artifacts_removal.laplasian_of_gaussian("path/to/image")
artifacts_removal.laplasian_of_gaussian(image_matrix)
artifacts_removal.dull_razor_artifact_removal(image, cc5)
artifacts_removal.morphological_closure_artifact_removal(image, cc5, True)
artifacts_removal.bothat_artifact_removal(image, cc5)
```

### Ajuste de contraste

La mejora del contraste realza los bordes y mejora la calidad de la imagen acentuando la
diferencia en intensidad del fondo, que serı́a la piel sana, y el frente de la 
imagen, que serı́a la lesión. Se encuentran los métodos:

- Ecualizacion Clásica del Histograma (equalize_histogram)
    > Ecualizacion clásica por cada canal
    >
    >**:param** image: Dirección a la imagen o matriz 3D representando una imagen en RGB
    >
    >**:return:** Imagen resultante de mezclar cada canal RGB despues de aplicar ecualización clásica
    >
- clahe
    > Ecualizacion adaptativa del histograma limitada por el contraste 
          (**C**ontrast **L**imited **A**daptive **H**istogram **E**qualization).
    >
    > Aplica CLAHE a cada canal RGB y luego mezcla los resultados.
    >
    >**:param** image:  Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** clip_limit: Umbral para el límite del contraste.
    >
    >**:param** tile_grid_size: Tamaño de la matriz para la ecualización del histograma. 
          La imagen original será dividida en pedazos rectangulares de igual tamaño, este parámetro 
          define la cantidad de pedazos por fila y por columna.
    >
    >**:return:** Imagen resultante de la mezcla de aplicar el algoritmo CLAHE a cada canal RGB
          y luego mezclar los resultados.
    >
- automatic_brightness_and_contrast
    > Ajusta automáticamente el brillo y el contraste de la imagen haciendo uso del histograma
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** clip_histogram_percent: Porciento de acumulacion del histograma.
    >
    >**:return:** Imagen con contraste y brillo mejorados.
    >
- window_enhancement
    > Mejora el contraste de una imagen en escala de grises modificando su histograma en un rango.
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** window_min: Rango mínimo de la ventana.
    >
    >**:param** window_max: Rango máximo de la ventana.
    >
    >**:return:** Imagen en escala de grises con el contraste mejorado.
    >
- histogram_bimodality
    > Mejora del contraste maximizando la medida de bimodalidad del histograma.
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** weights: Tupla de 3 valores o array de tuplas representando el peso de cada canal RGB.
    La suma de los valores en cada tupla debe ser 1. Ej: [(0.6,0.2,0.2),(0.4,0.4,0.2)]
    Evitar el uso del valor 0 para las tuplas. 
    >
    >**:return:** Imagen con el contraste mejorado.
- morphological_contrast_enhancement
    > Mejora del contraste usando operaciones morfológicas. Toma la imagen original y le suma 
        la imagen resultante de aplicar la opercion Top-Hat a la misma y luego le resta la imagen
        resultante de aplicarle Bottom-Hat
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** kernel: Núcleo a utilizar
    >
    >**:return:** Imagen con el contraste mejorado
    >
- reverse_morphological_contrast_enhancement
    > Mejora del contraste usando operaciones morfológicas. Toma la imagen original y le resta 
        la imagen resultante de aplicar la operación Top-Hat a la misma y luego le suma la imagen
        resultante de aplicarle Bottom-Hat
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** kernel: Núcleo a utilizar
    >
    >**:return:** Imagen con el contraste mejorado
    >

Ejemplo de uso:

```python
from dermoscopy_preprocessing import contrast
from dermoscopy_preprocessing.utils import WEIGTHS
from dermoscopy_preprocessing.utils import CIRCLE_KERNEL_3X3, RHOMB_KERNEL_3X3


contrast.equalize_histogram("path/to/image")
contrast.equalize_histogram(image_matrix)
contrast.clahe(image,4,(3,3))
contrast.window_enhancement(image,50,200)
contrast.histogram_bimodality(image, [(0.2,0.2,0.6),(0.3,0.3,0.4)])
contrast.histogram_bimodality(image,WEIGTHS)
contrast.morphological_contrast_enhancement(image,CIRCLE_KERNEL_3X3)
contrast.reverse_morphological_contrast_enhancement(image,RHOMB_KERNEL_3X3)
```
> **_Nota:_** Aquí solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Realce de bordes
La mejora de bordes permite una mejor visualización de los detalles de la lesión. 
Esta mejora de bordes se lleva acabo realizando operaciones de filtrado sobre la matriz.
Se encuentran los métodos:

- sharpen
    > Filtra los canales RGB de la imagen con un kernel resaltador de bordes.
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** kernel: Núcleo resaltador de bordes.
    >
    >**:return:** Imagen resultante con los bordes resaltados
- laplacian
    > Resalta los bordes substrayendo a cada canal RGB su laplaciano 
      y luego mezclando los resultados.
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:return:** Imagen resultante con los bordes resaltados
- unsharp_filter
    > Resaltado de bordes mediante la obtención de una imagen con bordes suavizados que se substrae de la
      imagen original. Luego el resultado es la imagen original más la imagen obtenida 
      anteriormente multiplicada por un factor (k).
   >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** k: Factor de multiplicación
    >
    >**:return:** Imagen con los bordes resaltados

Ejemplo de uso:

```python
from dermoscopy_preprocessing import edges
from dermoscopy_preprocessing.utils import SHARPEN_KERNEL

# retorna la imagen con los brdes resaltados usando el laplaciano
edges.laplacian("path/to/image")
edges.laplacian(image_matrix)
edges.sharpen(image, SHARPEN_KERNEL)
edges.unsharp_filter(image, 2)
```

> **_Nota:_** Aquí solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Ajuste de iluminación

Se encuentran los métodos:

- mul_log_brightness_enhancement
    > Mejora del brillo utilizando la multiplicación en el espacio logarítmico
    >
    >**:param** image:  Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** factor: Factor de multiplicación
    >
    >**:return:** Imagen con el brillo de cada uno de los canales RGB mejorado
- automatic_brightness_and_contrast
    > Ajusta automáticamente el brillo y el contraste de la imagen haciendo uso del histograma
    >
    >**:param** image: Dirección a la imagen o una lista 3D representando la imagen con sus tres canales.
    >
    >**:param** clip_histogram_percent: Porciento de acumulación del histograma.
    >
    >**:return:** Imagen con contraste y brillo mejorados.
    >
Ejemplo de uso:

```python
from dermoscopy_preprocessing import ilumination

ilumination.mul_log_brightness_enhancement("path/to/image", factor= 4)
ilumination.mul_log_brightness_enhancement(image_matrix, factor= 4)
ilumination.automatic_brightness_and_contrast(image, 15)
```

> **_Nota:_** Aquí solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Útiles

Se brindan kernels para facilitar el trabajo con los métodos de procesamiento de los cuales se emplearon
algunos como ejemplo en los metodos anteriores

- RHOMB_KERNEL_3X3
- STAR_KERNEL_3X3
- CIRCLE_KERNEL_3X3
- CIRCLE_KERNEL_4X4
- CIRCLE_KERNEL_5X5
- CIRCLE_KERNEL_7X7
- CIRCLE_KERNEL_9X9
- CIRCLE_KERNEL_11X11
- SHARPEN_KERNEL

Ejemplo de uso:

```python
from dermoscopy_preprocessing.utils import CIRCLE_KERNEL_5X5
```

## License

[MIT](htttp://choosealicense.com/licenses/mit/)
