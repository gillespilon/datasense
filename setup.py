from glob import glob
from setuptools import setup, find_packages


setup(
    name="datasense",
    version="0.9.1",
    packages=find_packages(),
    description="functions for datasense",
    url="https://github.com/gillespilon/datasense",
    install_requires=[
        "basis_expansions",
        "cached_property",
        "beautifultable",
        "scikit-learn",
        "statsmodels",
        "matplotlib",
        "pyautogui",
        "openpyxl",
        "psycopg2",
        "pyqrcode",
        "tabulate",
        "pyarrow",
        "dirsync",
        "psutil",
        "pandas",
        "numpy",
        "pypng",
        "scipy",
    ],
    author="Gilles Pilon",
    author_email="gillespilon13@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
    license="License :: OSI Approved :: ISC License (ISCL)",
    setup_requires=[
        # run pytest, coverage and checks when running python setup.py test.
        "pytest-runner",
        "pytest-cov",
    ],
    scripts=glob("bin/*"),
)
