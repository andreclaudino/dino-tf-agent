from setuptools import setup

setup(
    name='dino_ia',
    version='0.1',
    url='',
    license='',
    author='André Claudino',
    author_email='',
    description='',
    install_requires=[
        "flask",
        "python-socketio",
        "tf-agents-nightly",
        "tensorflow==2.0.0-beta0",
        "requests"
    ],
    tests_require=['pytest']
)
