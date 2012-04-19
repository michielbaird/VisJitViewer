#!/usr/bin/env pypy-c

from setuptools import setup

setup(name='JitViewer',
      version='0.1',
      description="Viewer for pypy's jit traces",
      author='Maciej Fijalkowski, Antonio Cuni and the PyPy team',
      author_email='fijall@gmail.com',
      url='http://pypy.org',
      packages=['_jitviewer'],
      scripts=['bin/jitviewer.py', 'bin/qwebview.py'],
      install_requires=['flask', 'pygments', 'simplejson', 'Jinja2>=2.6'],
      include_package_data=True,
      package_data={'': ['templates/*.html', 'static/*']},
      zip_safe=False)
