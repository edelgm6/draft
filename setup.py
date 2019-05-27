from setuptools import setup

setup(
    name='draft',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'mistune'
    ],
    entry_points='''
        [console_scripts]
        draft=draft.cli:main
    ''',
)
