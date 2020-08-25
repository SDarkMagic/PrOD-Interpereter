import setuptools
import pathlib

with open("README.md", "r") as desc:
    long_description = desc.read()


setuptools.setup(
    name="bwlpprod",
    version="1.1.1",
    author="SDarkMagic",
    author_email="TheSDarkMagic@gmail.com",
    description="A program for decoding and re-encoding Nintendo's PrOD file format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SDarkMagic/PrOD-Interpereter",
    include_package_data=True,
    packages=['blwp'],
    entry_points={
        'console_scripts': ['blwp_to_yml=blwp.blwp_to_yml:main', 'yml_to_blwp=blwp.yml_to_blwp:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "oead>=1.1.1",
    ],
)