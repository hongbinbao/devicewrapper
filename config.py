#!/usr/bin/python
# -*- coding:utf-8 -*- 

import os, sys
DEFAULT_RIGHT_DIR_NAME = 'pics'
DEFAULT_REPORT_DIR_NAME = 'report'
 
class Config(object):
    '''Instances of Config are used to configure behavior of device wrapper object.'''

    def __init__(self, **kw):
        self.env = kw.pop('env', {})
        self.working_dir = os.getcwd()
        self.right_dir_path = os.path.join(self.working_dir, DEFAULT_RIGHT_DIR_NAME)
        self.report_dir_path = os.path.join(self.working_dir, DEFAULT_REPORT_DIR_NAME)
        self._default = self.__dict__.copy()
        self.update(kw)
        self._orig = self.__dict__.copy()


    def default(self):
        '''Reset all config values to defaults.'''
        self.__dict__.update(self._default)

    def reset(self):
        self.__dict__.update(self._orig)

    def todict(self):
        return self.__dict__.copy()

    def update(self, d):
        self.__dict__.update(d)

    def __repr__(self):
        d = self.__dict__.copy()
        # don't expose env, could include sensitive info
        #d['env'] = {}
        keys = [ k for k in d.keys() if not k.startswith('_') ]
        keys.sort()
        return "Config(%s)" % ', '.join([ '%s=%r' % (k, d[k]) for k in keys ])

    __str__ = __repr__

    def __getitem__(self, name):
        if not hasattr(self, name):
            raise KeyError('Non-existing argument \'%s\'' % name)
        return getattr(self, name)

    def __setitem__(self, name, value):
        if not hasattr(self, name):
            raise KeyError('Non-existing argument \'%s\'' % name)
        setattr(self, name, value)


configer = Config(env=os.environ)
if __name__ == '__main__':
    configer = Config(env=os.environ)
    print configer
    print configer['working_dir']
    print configer.env['PWD']
    print configer['right_dir_path']
    print configer['report_dir_path']

