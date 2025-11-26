from setuptools import setup

setup(
    name="simstream",
    version="0.1.0",
    description="Bundled noVNC runner and helpers",
    # When publishing the `simstream/` directory as the project root, map the
    # package name `simstream` to this directory (the package files live here).
    packages=["simstream"],
    package_dir={"simstream": "."},
    include_package_data=True,
    package_data={
        "simstream": [
            "start_server.sh",
            "noVNC/**",
            ".fluxbox/**",
        ],
    },
    entry_points={
        "console_scripts": [
            "simstream-start=simstream.runner:main",
        ],
    },
    classifiers=["Programming Language :: Python :: 3"],
)
