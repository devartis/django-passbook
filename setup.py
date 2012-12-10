from distutils.core import setup

version = __import__('django_passbook').__version__

setup(
    name='django-passbook',
    version=version,
    author='Fernando Aramendi',
    author_email='fernando@devartis.com',
    packages=['django_passbook', ],
    url='http://github.com/devartis/django-passbook/',
    license=open('LICENSE.txt').read(),
    description='Django Passbook server app',
    long_description=open('README.md').read(),

    download_url='http://pypi.python.org/packages/source/D/django-passbook/django-passbook-%s.tar.gz' % version,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
