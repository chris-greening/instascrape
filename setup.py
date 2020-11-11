import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="insta-scrape",
    version="1.2.2",
    author="Chris Greening",
    author_email="chris@christophergreening.com",
    description="Super lightweight Instagram web scraper for data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chris-greening/instascrape",
    packages=["instascrape", "instascrape.core", "instascrape.scrapers"],
    install_requires=["requests", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
