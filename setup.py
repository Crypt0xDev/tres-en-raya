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
            'tres-en-raya-local=local.main:main',
            'tres-en-raya-web=web.app:run',
            'tres-en-raya-multiplayer=multiplayer.server:main',
        ],
    },
    include_package_data=True,
    description='A Tic Tac Toe game with local, web, and multiplayer versions.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/tres-en-raya-game',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
    ],
)