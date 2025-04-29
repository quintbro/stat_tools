from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

setup(
    name = 'statstools',
    version = '0.0.1',
    description = 'A package to aid in statistical analysis with statsmodels',
    author = 'Riley Wilkinson',
    author_email = 'quintbro@gmail.com',
    url = 'https://github.com/quintbro/stat_tools',
    packages=find_packages(),
    package_data = {'statstools': ['data/*.csv', 'assets/*']},
    install_requires = parse_requirements('requirements.txt')
)
