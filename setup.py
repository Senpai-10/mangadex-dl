from setuptools import setup

setup(
    name="mangadex-dl",
    version="0.0.1",
    install_requires=["requests", "rich", "python-slugify"],
    entry_points={"console_scripts": ["mangadex-dl=main:main"]},
)
