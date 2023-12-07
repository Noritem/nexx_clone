from setuptools import setup, find_packages

setup(
    name='nexx_clone',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'discord.py==1.7.3',
        'requests',
        'colorama',
        'psutil',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'nexx_clone=nexx_clone:main',
        ],
    },
    author='nexxrar',
    author_email='tech@moxx.tech',
    url='https://github.com/noritem/nexx_clone',  # Replace with the actual URL
    description='A Discord Selfbot for Clone Discord Server',
)
