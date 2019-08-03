from setuptools import setup, find_packages

setup(
    name = 'Drivy',
    version = '1.0',
    packages = find_packages(),
    package_data = {'Drivy': ['scripts/*.lua',]},
    entry_points = {'scrapy': ['settings = Drivy.settings']},
)