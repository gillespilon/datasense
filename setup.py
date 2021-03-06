from glob import glob
from setuptools import setup, find_packages


setup(
    name='datasense',
    description='functions for datasense',
    url='https://github.com/gillespilon/datasense',
    version='0.1',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'cached_property',
        'beautifultable',
        'basis-expansions',
        'sklearn',
        'dirsync',
    ],
    author='Gilles Pilon',
    author_email='gillespilon13@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
    license='License :: OSI Approved :: ISC License (ISCL)',
    setup_requires=[
        # run pytest, coverage and checks when running python setup.py test.
        'pytest-runner',
        'pytest-cov',
    ],
    scripts=glob('bin/*'),
)

