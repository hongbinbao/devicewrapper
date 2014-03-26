#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requires = ['uiautomator']

setup(name='devicewrapper',
      version='2.1.1',
      description='Python Wrapper for android uiautomator-server. provides more event inject and inspect way',
      long_description='''\
python wrapper of android uiautomator-server\n
dependency:\n
1: sudo apt-get install python-opencv\n
2: sudo apt-get install python-numpy\n
3: target android device: sdk_version>=16\n

usage:\n
>>> from devicewrapper.android import device as d\n
>>> d.info\n
>>> d.orientation
>>> d.orientation = 'l'
>>> d.wakeup()\n
>>> d.start_activity(action='android.intent.action.DIAL', data='tel:xxxx', flags=0x04000000)\n
>>> d.find('phone_launch_success.png') \n
>>> d.click(100, 200) \n
>>> d.click('DPAD_NUMBER_1.png') \n
>>> d.click('DPAD_NUMBER_1.png', rotation=90) \n
>>> d.exists(text='string_value_of_screen_layout_component_text_attribute') \n
>>> d.expect('phone_launch_success.png') \n
>>> d(text='Settings').click() \n
''',
      author='bao hongbin',
      author_email='hongbin.bao@gmail.com',
      install_requires=requires,
      packages = ['devicewrapper'],
      setup_requires=['uiautomator'],
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
