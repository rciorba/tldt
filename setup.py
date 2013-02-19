from setuptools import setup, find_packages

VERSION = 0.1

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="tldt",
    version=VERSION,
    url="http://github.com/rciorba/tldt",
    long_description=open('README.md', 'r').read(),
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 1 :: Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules'"],
    install_requires=requirements)
