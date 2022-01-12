from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Image Processing Package"
LONG_DESCRIPTION = "Image Processing techniques for enhance contrast, ilumination and edges." \
                   " Methods for artifacts removal. Focused mainly on demorscopic images"

setup(
    name="img_preprocessing",
    version=VERSION,
    author="Claudia Olavarrieta Martinez, Marcos A. Valdivie Rodriguez, Luis E. Dalmau Coopat",
    author_email="<claudiaomtnez@gmail.com>,<mavaldivie98@gmail.com>,<luke.dalmau@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["opencv-python", "numpy"],
    keywords=["python","computer vision","images","dermoscopy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"

    ]
)