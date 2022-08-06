import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sfdutf7",
    version="0.0.1",
    author="Fredrick Brennan",
    author_email="copypaste@kittens.ph",
    description="SFDUTF7 encoding parsing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ctrlcctrlv/sfdutf7.py",
    entry_points = {'console_scripts': ['sfdutf7 = sfdutf7.__main__:main'],},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
