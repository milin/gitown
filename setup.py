#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pre-commit',
    'invoke',
    'simplejson'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Milind Shakya",
    author_email='sh.milind@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Keep your github CODEOWNERS file up to date.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gitown',
    name='gitown',
    packages=find_packages(include=['gitown', 'gitown.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/milin/gitown',
    version='0.1.8',
    entry_points={
        'console_scripts': [
            'gitown = gitown.gitown:main',
        ]
    },
    zip_safe=False,
)
