from setuptools import setup, find_packages

setup(
    name='movie_list_retriever',
    version='0.12',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'playwright',
        'typed_argument_parser @ git+https://github.com/vphpersson/typed_argument_parser.git#egg=typed_argument_parser'
    ]
)
