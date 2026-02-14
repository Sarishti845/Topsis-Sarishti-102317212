from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="Topsis-Sarishti-102317212",
    version="1.0.0",
    author="Sarishti",
    author_email="ssarishti_be23@thapar.edu",
    description="A Python package for solving TOPSIS MCDM problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sarishti845/Topsis-Sarishti-102317212",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_sarishti.topsis:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
