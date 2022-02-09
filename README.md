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

#### Artefactos

Se encuentran los métodos:
 
- morphological_closure_artifact_removal
- dull_razor_artifact_removal
- bothat_artifact_removal
- laplasian_of_gaussian
- clean_remaining_artifacts

Ejemplo de uso:
```python
from img_preprocessing import artifacts_removal

# returns image with contrast improved using histogram equalization method
artifacts_removal.laplasian_of_gaussian("path/to/image")
artifacts_removal.laplasian_of_gaussian(image_matrix)
```


#### Contraste

Se encuentran los métodos:
 
- equalize_histogram
- clahe
- automatic_brightness_and_contrast
- window_enhancement
- histogram_bimodality
- morphological_contrast_enhancement
- reverse_morphological_contrast_enhancement

Ejemplo de uso:
```python
from img_preprocessing import contrast

# returns image with contrast improved using histogram equalization method
contrast.equalize_histogram("path/to/image")
contrast.equalize_histogram(image_matrix)
```

#### Bordes

Se encuentran los métodos:
 
- sharpen
- laplacian
- unsharp_filter

Ejemplo de uso:
```python
from img_preprocessing import edges

# returns image with contrast improved using histogram equalization method
edges.laplacian("path/to/image")
edges.laplacian(image_matrix)
```

#### Iluminación

Se encuentran los métodos:
 
- mul_log_brightness_enhancement
- automatic_brightness_and_contrast
- unsharp_filter

Ejemplo de uso:
```python
from img_preprocessing import ilumination

# returns image with contrast improved using histogram equalization method
ilumination.mul_log_brightness_enhancement("path/to/image", 4)
ilumination.mul_log_brightness_enhancement(image_matrix, 4)
```


#### Utiles

Se brindan kernels para facilitar el trabajo con los métodos de procesamiento
 
- RHOMB_KERNEL_3X3
- STAR_KERNEL_3X3
- CIRCLE_KERNEL_3X3
- CIRCLE_KERNEL_4X4
- CIRCLE_KERNEL_9X9
- CIRCLE_KERNEL_5X5
- CIRCLE_KERNEL_7X7
- CIRCLE_KERNEL_11X11
- SHARPEN_KERNEL

Ejemplo de uso:
```python
from img_preprocessing.utils import CIRCLE_KERNEL_5X5
```

## License 
[MIT](htttp://choosealicense.com/licenses/mit/)