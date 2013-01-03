from distutils.core import setup


setup(
    name = 'django-simple-templates',
    description = 'Easy, designer-friendly templates and A/B testing friendly tools for Django.',
    long_description=u'View `django-simple-templates documentation on Github  <https://github.com/jaddison/django-simple-templates>`_.',
    author='James Addison',
    author_email='code@scottisheyes.com',
    packages = ['simple_templates'],
    version = '0.6.0',
    url='http://github.com/jaddison/django-simple-templates',
    keywords=['a/b testing', 'split testing', 'a/b', 'split'],
    license='BSD',
    classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: BSD License',
      'Intended Audience :: Developers',
      'Environment :: Web Environment',
      'Programming Language :: Python',
      'Framework :: Django',
      'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)