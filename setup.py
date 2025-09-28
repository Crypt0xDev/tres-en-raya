from setuptools import setup, find_packages

setup(
    name='tres-en-raya-game',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'requests',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'tres-en-raya-cli=src.interfaces.cli.main:main',
            'tres-en-raya-web=src.interfaces.web.app:run',
            'tres-en-raya-multiplayer=src.multiplayer.server:main',
        ],
    },
    include_package_data=True,
    description='A Tic Tac Toe game with local, web, and multiplayer versions with AI opponent.',
    author='Crypt0xDev',
    author_email='alexis.alvarado@unsm.edu.pe',
    url='https://github.com/Crypt0xDev/tres-en-raya',
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)