import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfbuilder", # Replace with your own username
    version="0.0.1",
    author="Alessandro Atria",
    author_email="a.atria@gmail.com",
    description="DataFrame builder for financial time series data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "tsp"},
    packages=setuptools.find_packages(exclude=("tests")),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.18.4",
        "pandas>=1.1.5"
    ]
)