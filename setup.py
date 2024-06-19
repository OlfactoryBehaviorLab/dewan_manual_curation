from setuptools import setup, find_packages

setup(
    name='dewan_manual_curation',
    description='DewanLab Manual Curation Interface',
    version='2.0',
    author='Austin Pauley, Dewan Lab, Florida State University',
    author_email='olfactorybehaviorlab@gmail.com',
    url='https://github.com/OlfactoryBehaviorLab/dewan_manual_curation',
    packages=['dewan_manual_curation'],
    python_requires=">=3.7, <3.11",
    install_requires=[
        'numpy',
        'pandas>2.0.0',
        'matplotlib',
        'scikit-learn',
        'pyarrow',
        'PySide6>=6.5.0',
        'PyQtDarkTheme',
        'Shapely',
    ]
)
