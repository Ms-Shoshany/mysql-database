from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mysql-database',
    version='0.1.6',
    packages=find_packages(),
    install_requires=['mysql-connector-python'],
    author='hanna',
    author_email='channashosh@gmail.com',
    description='easy calls to mysql databases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ms-Shoshany/mysql-database',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
