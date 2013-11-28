#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requires = ['imglib', 'uiautomator']

setup(name='devicewrapper',
      version='1.5',
      description='Python Wrapper for android uiautomator and imglib',
      long_description='''\
python wrapper of uiautomator\n
usage:\n
>>> from devicewrapper.android import device as d\n
>>> d.info()\n
>>> d.wakeup()\n
>>> d.start_activity(action='android.intent.action.DIAL', data='tel:xxxx', flags=0x04000000)\n
>>> d.find('phone_launch_success.png') \n
>>> d.exists(text='string_value_of_screen_layout_component_text_attribute') \n
>>> d.expect('phone_launch_success.png') \n
''',
      author='bao hongbin',
      author_email='hongbin.bao@gmail.com',
      install_requires=requires,
      packages = ['devicewrapper'],
      setup_requires=['imglib', 'uiautomator'],
      license='MIT',
      platforms='any',
      classifiers=(
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Testing',
            )
      )
