from pathlib import Path
from setuptools import setup, find_packages

# Extracts the long description from the README.md file.
DESCRIPTION_FILE = Path("./README.md").absolute()
DESCRIPTION = DESCRIPTION_FILE.read_text()

# Extracts the version from the pyweather/version.py file.
VERSION_FILE = Path("./pyweather/version.py").absolute()
VERSION = VERSION_FILE.read_text().strip().replace("version = ", "").replace('"', "")

setup(
    name="pyweather",
    version=VERSION,
    author="rahul4732saini",
    license="MIT",
    description="Versatile weather package for effortless meteorology data extraction.",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://www.github.com/rahul4732saini/pyweather",
    keywords="pyweather, weather, pandas, open-meteo",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Meteorology :: Weather",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    platforms=["any"],
    install_requires=[
        "certifi==2024.2.2",
        "charset-normalizer==3.3.2",
        "idna==3.7",
        "numpy==1.26.4",
        "pandas==2.2.2",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "requests==2.31.0",
        "six==1.16.0",
        "tzdata==2024.1",
        "urllib3==2.2.1",
    ],
)