import setuptools
import pgaudi

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgaudi",
    version="1.0.0",
    description=pgaudi.__description__,
    long_description=long_description,
    author=pgaudi.__author__,
    author_email="andresgineranton@outlook.com",
    packages=setuptools.find_packages(),
    url="https://github.com/andresginera/compare-equal",
    license="Apache Software License",
    entry_points={"console_scripts": ["pgaudi=pgaudi.main:main"]},
)
