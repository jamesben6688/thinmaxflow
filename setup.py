import os
import urllib.request
from zipfile import ZipFile
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


class LazyCythonize(list):
    def __init__(self, callback):
        self._list, self.callback = None, callback

    def c_list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list

    def __iter__(self):
        for e in self.c_list():
            yield e

    def __getitem__(self, ii): return self.c_list()[ii]

    def __len__(self): return len(self.c_list())


def extensions():

    numpy_include_dir = np.get_include()

    maxflow_module = Extension(
        "thinmaxflow._maxflow",
        [
            "thinmaxflow/src/_maxflow.pyx",
            "thinmaxflow/src/core/maxflow.cpp",
            "thinmaxflow/src/core/graph.cpp",
        ],
        language="c++",
        include_dirs=[
            numpy_include_dir,
        ]
    )
    return cythonize([maxflow_module])


setup(name="thinmaxflow",
      version="0.1.0",
      author="Niels Jeppesen",
      author_email="niejep@dtu.dk",
      description="A thin Maxflow wrapper for Python",
      url="https://github.com/Skielex/thinmaxflow",
      license="GPL",
      long_description="""
      
      """,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: C++",
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering :: Image Recognition",
          "Topic :: Scientific/Engineering :: Artificial Intelligence",
          "Topic :: Scientific/Engineering :: Mathematics"
      ],
      packages=["thinmaxflow"],
      ext_modules=LazyCythonize(extensions),
      requires=["numpy", "Cython"],
      setup_requires=['numpy', 'Cython']
      )
