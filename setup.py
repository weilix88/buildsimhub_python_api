import setuptools
from io import open


__version__ = None
with open('BuildSimHubAPI/version.py') as f:
    exec(f.read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BuildSimHubAPI",
    version=str(__version__),
    author="Weili Xu, Haopeng Wang",
    author_email="weili.xu@buildsimhub.net",
    url="https://github.com/weilix88/buildsimhub_python_api",
    description="BuildSim Cloud API library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(exclude=['test', 'modelingstandard', 'workflowexample']),
    include_package_data=True,
    package_Data={'BuildSimHubAPI': ['BuildSimHubAPI/info.config']},
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
