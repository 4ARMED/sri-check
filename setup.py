import os, re, setuptools

def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)
    return open(path, mode=mode, encoding=encoding)

with open_local(["sricheck", "__init__.py"]) as f:
    version = re.search(r"__version__ = [\"'](\d+\.\d+\.\d+)[\"']", f.read()).group(1)

with open_local(["README.md"]) as f:
    long_description = f.read()

install_requires = [
    "beautifulsoup4>=4.0",
    "lxml>=4.8",
    "requests>=2.0",
    "selenium>=4.8"
]

setuptools.setup(
    name="sri-check",
    author="Marc Wickenden",
    author_email="code@4armed.com",
    description="Subresource Integrity Checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4armed/sri-check",
    version=version,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["sri-check=sricheck.sricheck:cli"]},
    test_suite="tests"
)