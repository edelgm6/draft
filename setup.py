from setuptools import setup, find_packages
import io

long_description = io.open('README.rst', encoding='utf-8').read()

setup(
    name="draft-cli",
    version="0.1.1",
    author="Garrett Edel",
    author_email="edelgm6@gmail.com",
    description="CLI-enabled writing system to keep your work modular and optimize your files for git for version control.",
    long_description=long_description,
    url="https://github.com/edelgm6/draft",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "PyYAML",
        "mistune"
    ],
    entry_points='''
        [console_scripts]
        draft=draft.cli:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
