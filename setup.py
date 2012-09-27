from setuptools import setup, find_packages
import os

version = '0.5'

long_description = (open('README.rst').read() + '\n')

setup(name='il.portalinterlegis',
      version=version,
      description="Portal Interlegis",
      long_description=long_description,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        ],
      keywords='web zope plone theme skin portal interlegis',
      author='Interlegis',
      author_email='spdt@interlegis.leg.br',
      url='http://www.interlegis.leg.br/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['il', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'five.grok',
          'plone.app.theming',
          'plone.directives.form',
          'plone.app.z3cform',
          'plone.formwidget.contenttree',
          'plone.formwidget.autocomplete',
          'Jinja2', # This one is not neurotic about missing values. We need this.
          'collective.js.jqueryui',
          'feedparser',
          'sc.contentrules.groupbydate',
      ],
      extras_require={'test': ['plone.app.testing', 'mock']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
