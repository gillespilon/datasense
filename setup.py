from glob import glob
from setuptools import setup


setup(
    name='datasense',
    description='functions for data sense',
    url='https://github.com/gillespilon/datasense',
    version='0.1',
    install_requires=[
        'regex',
    ],
    author='Gilles Pilon',
    author_email='gillespilon13@gmail.com',
    packages=['datasense'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    setup_requires=[
        # run pytest, coverage and checks when running python setup.py test.
        'pytest-runner',
        'pytest-cov',
        'pytest-flakes',
    ],
    tests_require=[
        'pytest',
        'coverage',
    ],
    scripts=glob('bin/*'),
    license='ISC',
)

