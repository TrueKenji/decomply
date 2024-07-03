from setuptools import setup, find_packages

setup(
    name='decomply',
    version='1.1.0',
    packages=find_packages(),
    description='decomply allows unified processing of nested dictionaries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # for Markdown
    author='TrueKenji',
    url='https://github.com/truekenji/decomply',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=['Dictionary', 'Recursive', 'Traverse', 'Apply',
              'Decompose', 'Partition', 'Nested', 'Loop', 'List', 'JSON']
)
