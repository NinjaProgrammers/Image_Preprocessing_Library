from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
VERSION = '0.0.1'
DESCRIPTION = "Image Processing Package"
LONG_DESCRIPTION = (HERE / "README.md" ).read_text(encoding='utf-8')
LONG_DESCRIPTION_TYPE = "text/markdown"

setup(
    name="img_preprocessing",
    version=VERSION,
    author="Claudia Olavarrieta Martinez, Marcos A. Valdivie Rodriguez, Luis E. Dalmau Coopat",
    author_email="<claudiaomtnez@gmail.com>,<mavaldivie98@gmail.com>,<luke.dalmau@gmail.com>",
    url="https://github.com/ClaudiaOM/Image_Preprocessing_Library",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    packages=find_packages(),
    install_requires=["opencv-python", "numpy"],
    keywords=["python", "computer vision", "images", "dermoscopy"]
)
