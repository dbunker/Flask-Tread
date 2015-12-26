"""
Flask-Tread
-----------

Library for Flask route input and output validation, authentication and transformation
"""
from setuptools import setup

setup(
    name='Flask-Tread',
    version='0.1',
    url='http://github.com/dbunker/Flask-Gasket',
    license='ISC',
    description='Library for Flask route input and output validation, authentication and transformation',
    py_modules=['flask_tread'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'passlib',
        'hashids'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
