"""Configuration du package AuditronAI."""
import os
from setuptools import setup, find_packages

# Lire le README.md pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lire les dépendances depuis requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="auditronai",
    version="1.0.0",
    author="AuditronAI Team",
    author_email="contact@auditronai.com",
    description="Système d'analyse de code multi-langage pour la sécurité et la qualité",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/AuditronAI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Natural Language :: French",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-asyncio>=0.16.0',
            'pytest-cov>=2.12.1',
            'pytest-mock>=3.6.1',
            'black>=21.9b0',
            'isort>=5.9.3',
            'mypy>=0.910',
            'pylint>=2.11.0',
            'sphinx>=4.2.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
        'typescript': [
            'typescript>=4.4.0',
            'eslint>=8.0.0',
            '@typescript-eslint/parser>=5.0.0',
            '@typescript-eslint/eslint-plugin>=5.0.0',
            'eslint-plugin-security>=1.4.0',
        ],
        'sql': [
            'sqlparse>=0.4.2',
            'psycopg2-binary>=2.9.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'auditronai=AuditronAI.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'AuditronAI': [
            'templates/*.yaml',
            'configs/*.yaml',
        ],
    },
    data_files=[
        ('configs', ['configs/analyzer_config.yaml']),
    ],
    project_urls={
        'Bug Reports': 'https://github.com/votre-username/AuditronAI/issues',
        'Source': 'https://github.com/votre-username/AuditronAI',
        'Documentation': 'https://auditronai.readthedocs.io/',
    },
    keywords=[
        'security',
        'code-analysis',
        'static-analysis',
        'quality-assurance',
        'typescript',
        'sql',
        'python',
        'linting',
        'vulnerability-detection',
        'code-quality',
    ],
)
