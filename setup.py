from setuptools import find_packages, setup

setup(
    name="VicSM",
    verision="1.0.1",
    author="Christopher Poulsen",
    author_email="chris30-1@hotmail.com",
    description="Una aplicación para producir recibos y llevar registro de productos y clientes ",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "sqlalchemy"
    ]
)