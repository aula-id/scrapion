"""Setup script for scrapion package (backwards compatibility)"""

from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapion",
    version="0.1.1",
    author="Aula Dev",
    author_email="contact@aula.id",
    description="Web scraping automation system with intelligent fallback mechanisms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aula-id/scrapion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "fake-useragent>=1.4.0",
        "markdownify>=0.11.0",
        "pyvirtualdisplay>=3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "scrapion=scrapion.cli:main",
        ],
    },
)
