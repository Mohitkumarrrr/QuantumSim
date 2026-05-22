"""Setup configuration for QuantumSim."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantumsim",
    version="1.0.0",
    author="Mohit Kumar",
    author_email="mohit.kumar@example.com",
    description="A quantum mechanics simulator with visualization for quantum computing education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohitkumar/quantumsim",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
)
