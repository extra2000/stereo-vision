import os
import subprocess as sp
from setuptools import setup, find_packages

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def _get_version():
    # Credits to https://packaging.python.org/guides/single-sourcing-package-version/
    version = {}
    with open("stereo_vision/version.py") as fp:
        exec(fp.read(), version)
    return version['version']

def _get_long_description():
    with open(os.path.join(PROJECT_ROOT, 'README.md'), 'r', encoding='utf-8') as f:
        long_description = f.read()
    return long_description

def _setup_package():
    setup(
        name='stereo_vision',
        version=_get_version(),
        description='Stereo Vision project',
        long_description=_get_long_description(),
        author='extra2000',
        author_email='extra2000',
        keywords='computer vision',
        include_package_data=True,
        package_data={},
        packages=[
            'stereo_vision',
            'stereo_vision.console',
        ],
        entry_points={
            'console_scripts': [
                'stereovision=stereo_vision.console:main',
            ],
        },
        python_requires='>=3.6',
        install_requires=[
            'opencv-python-headless >=4.5.0, ==4.5.*',
        ],
        classifiers=[],
        project_urls={
            'Source': 'https://github.com/extra2000/stereo-vision',
            'Bug Reports': 'https://github.com/extra2000/stereo-vision/issues',
        },
        setup_requires=[],
    )

if __name__ == '__main__':
    _setup_package()
