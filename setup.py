from setuptools import setup
from v2checkin import config

with open('README.md') as f:
    long_description = f.read()

setup(
    name='v2checkin',
    description='Yet another checkin tool for v2ex.',
    version=config.VERSION,
    license='MIT',
    author='Timothy Qiu',
    packages=[
        'v2checkin',
        'v2checkin.providers'
    ],
    package_data={
        'v2checkin': ['README.md', 'LICENSE']
    },
    install_requires=['requests', 'lxml'],
    entry_points={
        'console_scripts': [
            'v2checkin = v2checkin.checkin:main',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=long_description
)
