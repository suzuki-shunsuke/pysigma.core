from setuptools import setup, find_packages


setup(
    name="sigma.core",
    version="0.2.0a0",
    packages=["sigma", "sigma.core"],
    namespace_packages=["sigma"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[],
    extras_require={},
    zip_safe=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst", "*.md"]
    },
    author="Suzuki Shunsuke",
    author_email="suzuki.shunsuke.1989@gmail.com",
    description="Validation framework.",
    license="MIT",
    keywords="validation",
    url="https://github.com/pysigma/core",
)
