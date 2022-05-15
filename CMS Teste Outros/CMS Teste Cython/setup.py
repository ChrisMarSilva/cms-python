# from distutils.core import setup, Extension
# from Cython.Build import cythonize
# exts = cythonize([Extension(name='c_fib_import', sources=['c_fib.c', 'c_fib_import.pyx'])])
# setup(ext_modules=exts)

from setuptools import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("fib_cy.py"))
setup(ext_modules = cythonize("fib_x.pyx"))

# cythonize -a -i fib_py_orig.py
# python -m easycython fib_py_orig.py

# python setup.py build_ext --inplace
