# Preprocesamiento de Imágenes



## img_preprocessing

El objetivo de esta librería es el preprocesamiento de imágenes de dermatoscopio. Se brindan métodos
para la mejora de contraste, bordes e iluminación. También se incluyen métodos para la eliminación
de artefactos. Su uso es exclusivo para imágenes de dermatoscopio, los resultados en otro tipo
de imágenes no se han comprobado.

## Autores

[Claudia Olavarrieta Martínez](https://github.com/ClaudiaOM)

[Marcos Adrián Valdivié Rodríguez](https://github.com/mavaldivie)

[Luis Enrique Dalmau Coopat](https://github.com/lukedalmau)

## Instalación

Como aún está en progreso el desarrollo de la librería solo se ofrece una version de prueba en testpypi

``
pip install -i https://test.pypi.org/simple/ img-preprocessing==0.0.1
``

Requiere como dependencias _opencv_ y _numpy_

## Uso

### Eliminación de artefactos

Se encuentran los métodos:

- morphological_closure_artifact_removal
    > Artifact removal using morphological closure
    >
    >    **:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >    **:param** kernel: Kernel
    >
    >    **:param** blur: True or False, indicates if a median blur should be applied before morphological closure
    >
    >    **:return:** Resulting image of merging RGB channels after morphological closure

- dull_razor_artifact_removal
    > Artifact Removal using Dull Razor method
    >
    >   **:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >   **:param** kernel: Kernel
    >
    >   **:return:** Resulting image of merging RGB channels after dull razor methd on each channel
    >
- bothat_artifact_removal
    > Artifact Removal using Bothat morphological operations
    >
    >   **:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >   **:param** kernel: Kernel
    >
    >   **:return:** Resulting image of merging RGB channels after bothat method on each channel
    >
- laplasian_of_gaussian
    > Artifact Removal using Laplassian of Gaussian method
    >
    >   **:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >   **:return:** Resulting image of merging RGB channels after bothat method on each channel
- clean_remaining_artifacts
    > **Method still on development. Use at own risk!**
    >
    >Remove remaining artifacts from image
    >
    >   **:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >   **:return:** Image

Utilizamos estos métodos para eliminar artefactos de una imagen de dermatoscopio, dígase cabellos, burbujas, etc.

Ejemplo de uso:

```python
from img_preprocessing import artifacts_removal

# returns image with the artifacts removed by laplasian of gaussian
artifacts_removal.laplasian_of_gaussian("path/to/image")
artifacts_removal.laplasian_of_gaussian(image_matrix)
```

> **_Nota:_** Aqui solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Ajuste de contraste

Se encuentran los métodos:

- equalize_histogram
    > Classical Histogram Equalization.
    >
    >Histogram Equalization for each RGB channel and merge the results
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:return:** Image from merging equalized histogram of RGB channels
    >
- clahe
    > Contrast Limited Adaptive Histogram Equalization.
    >
    >CLAHE applied to each RGB channel and results merged
    >
    >**:param** image:  Path to Image or 3D Matrix representing RGB image
    >
    >**:param** clip_limit: Threshold for contrast limiting.
    >
    >**:param** tile_grid_size: Size of grid for histogram equalization. Input image will be divided into
    equally sized rectangular tiles. tile_grid_size defines the number of tiles in row and column.
    >
    >**:return:** Image from merging clahe of RGB channels
    >
- automatic_brightness_and_contrast
    > Automatic contrast and image brightness calculated by cumulative function on image histogram
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** clip_histogram_percent:
    >
    >**:return:** Image with contrast and brightness enhanced
    >
- window_enhancement
    > Contrast enhancement of gray image by modifying histogram in a range
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** window_min: Minimal range of window
    >
    >**:param** window_max: Maximal range of window
    >
    >**:return:** Image in gray scale with contrast enhanced
    >
- histogram_bimodality
    > Contrast enhancement by maximizing histogram bimodality
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** weights: Tuple of 3 values or array of tuples for channels RGB.
    The sum of values must be 1. Ex: [(0.6,0.2,0.2),(0.4,0.4,0.2)]
    Avoid zero values for any of the channels
    >
    >**:return:** Image with contrast enhanced and best weight obtained
- morphological_contrast_enhancement
    > Contrast enhancement usign morphological operations
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** kernel: Morphological kernel
    >
    >**:return:** Original image plus tophat image of original minus bottomhat operation of original image
    >
- reverse_morphological_contrast_enhancement
    > Contrast enhancement usign morphological operations
    >
    >**:param** image:  Path to Image or 3D Matrix representing RGB image
    >
    >**:param** kernel: Morphological kernel
    >
    >**:return:** Original image minus tophat image of original plus bottomhat operation of original image
    >

Ejemplo de uso:

```python
from img_preprocessing import contrast

# returns image with contrast improved using histogram equalization method
contrast.equalize_histogram("path/to/image")
contrast.equalize_histogram(image_matrix)
```
> **_Nota:_** Aqui solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Realce de bordes

Se encuentran los métodos:

- sharpen
    > RGB channels filtering with edge sharpening kernel
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** kernel: Edge sharpening kernel
    >
    >**:return:** Resulting image from merging RGB filtered channels
- laplacian
    > Edge sharpening subtracting laplacian of RGB channels from original channels
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:return:** Resulting image from merging RGB filtered channels
- unsharp_filter
    > Edge enhancement with unsharp method
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** k: Multiplication factor
    >
    >**:return:** Original image plus image with edge enhanced

Ejemplo de uso:

```python
from img_preprocessing import edges

# returns image with all the edges enhanced by laplacian
edges.laplacian("path/to/image")
edges.laplacian(image_matrix)
```

> **_Nota:_** Aqui solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Ajuste de iluminación

Se encuentran los métodos:

- mul_log_brightness_enhancement
    > Brightness enhancement with multiplication on logarithm space
    >
    >**:param** image:  Path to Image or 3D Matrix representing RGB image
    >
    >**:param** factor: Multiplication Factor
    >
    >**:return:** Image with brightness enhanced in RGB channels
- automatic_brightness_and_contrast
    > Automatic contrast and image brightness calculated by cumulative function on image histogram
    >
    >**:param** image: Path to Image or 3D Matrix representing RGB image
    >
    >**:param** clip_histogram_percent:
    >
    >**:return:** Image enhanced, alpha and beta parameters

Ejemplo de uso:

```python
from img_preprocessing import ilumination

# returns image with ilumination improved using mul_log_brightness_enhancement
ilumination.mul_log_brightness_enhancement("path/to/image", mul_factor= 4)
ilumination.mul_log_brightness_enhancement(image_matrix, mul_factor= 4)
```

> **_Nota:_** Aqui solo le mostramos un ejemplo. Para obtener más información sobre los métodos, consulte el código.

### Utiles

Se brindan kernels para facilitar el trabajo con los métodos de procesamiento

- RHOMB_KERNEL_3X3
- STAR_KERNEL_3X3
- CIRCLE_KERNEL_3X3
- CIRCLE_KERNEL_4X4
- CIRCLE_KERNEL_5X5
- CIRCLE_KERNEL_7X7
- CIRCLE_KERNEL_9X9
- CIRCLE_KERNEL_11X11
- SHARPEN_KERNEL

Utilizamos algunos de estos kernels para facilitar el trabajo con los métodos de procesamiento y eliminación de artefactos, pero pueden ser utilizados para otros fines y es por ello que lo brindamos como una herramienta.

Ejemplo de uso:

```python
from img_preprocessing.utils import CIRCLE_KERNEL_5X5
```

## License

[MIT](htttp://choosealicense.com/licenses/mit/)
