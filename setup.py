from setuptools import setup, find_packages

setup(
    name='mysql-database',
    version='0.1.4',
    packages=find_packages(),
    install_requires=["mysql-connector-python"],
    author='hanna',
    author_email='channashosh@gmail.com',
    description='easy calls to mysql databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
