import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qqdm",
    version="0.0.2",
    author="KimythAnly",
    author_email="kimythanly@gmail.com",
    description="A multi-line logging toolkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimythanly/qqdm",
    packages=setuptools.find_packages(),
    install_requires=[
        'addict'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)