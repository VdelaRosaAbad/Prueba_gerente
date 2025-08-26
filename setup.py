#!/usr/bin/env python3
"""
📦 Archivo de configuración para Dataflow Pipeline
🔧 Instala todas las dependencias necesarias
"""

from setuptools import setup, find_packages

setup(
    name="ultra-fast-loader",
    version="1.0.0",
    description="Pipeline ultra-rápido para carga de 136GB en BigQuery",
    packages=find_packages(),
    install_requires=[
        'apache-beam[gcp]==2.48.0',
        'google-cloud-bigquery==3.11.4',
        'google-cloud-storage==2.10.0',
        'pandas==2.1.1',
        'numpy==1.24.3',
        'pyarrow==13.0.0',
        'fastparquet==2023.10.1',
    ],
    python_requires='>=3.8',
    author="Deacero Team",
    author_email="team@deacero.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
