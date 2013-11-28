#!/usr/bin/python
# -*- coding:utf-8 -*- 

import os, sys, time, types, shutil
from imglib.imgcomparison import isMatch, getMatchedCenterOffset
from devicewrapper.config import configer
from uiautomator import Device

__all__ = ['device']
ANDROID_SERIAL = 'ANDROID_SERIAL'

class AndroidDevice(object):
    '''
    wrapper for android uiautomator(pip install uiautomator) and image comparision(pip install imglib)
    to provide android device event inject and ui object inspect and image comparison.
    '''

    def __init__(self):
        self.serial = configer.env[ANDROID_SERIAL] if configer.env.has_key(ANDROID_SERIAL) else None
        self.d = Device(self.serial)
    
    def __getattr__(self, method):
        '''
        forward method to uiautomator device if method support by uiautomator.
        '''
        if hasattr(self.d, method):
            def wrapper(*args, **kwargs):
                return getattr(self.d, method)(*args, **kwargs)
            return wrapper
        raise AttributeError(method)


    def serial(self):
        '''device serial number from $ANDROID_SERIAL '''
        return self.serial

    def info(self):
        '''retrieve the device info'''
        return self.d.info
   
    def sleep(self, seconds):
        time.sleep(seconds)
        return self

    #device event inject
    def start_activity(self, **kwargs):
        '''launch application from android shell am start: component, flag
        // from adb docs:
        //<INTENT> specifications include these flags:
        //    [-a <ACTION>] [-d <DATA_URI>] [-t <MIME_TYPE>]
        //    [-c <CATEGORY> [-c <CATEGORY>] ...]
        //    [-e|--es <EXTRA_KEY> <EXTRA_STRING_VALUE> ...]
        //    [--esn <EXTRA_KEY> ...]
        //    [--ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE> ...]
        //    [-e|--ei <EXTRA_KEY> <EXTRA_INT_VALUE> ...]
        //    [-n <COMPONENT>] [-f <FLAGS>]
        //    [<URI>]
        '''
        #d.server.adb.cmd('shell','am', 'start', '-a', 'android.intent.action.DIAL','tel:13581739891').communicate()
        #sys.stderr.write(str(kwargs))
        keys = kwargs.keys()
        shellcmd = ['shell', 'am', 'start']
        if 'component' in keys:
            shellcmd.append('-n')
            shellcmd.append(kwargs['component'])

        if 'action' in keys:  
            shellcmd.append('-a')
            shellcmd.append(kwargs['action'])

        if 'data' in keys:
            shellcmd.append('-d')
            shellcmd.append(kwargs['data'])

        if 'mimetype' in keys:
            shellcmd.append('-t')
            shellcmd.append(kwargs['mimetype'])

        if 'categories' in keys:
            for category in kwargs['categories']:
                shellcmd.append('-c')
                shellcmd.append(category)
        
        if 'extras' in keys:
            for extra_key, extra_value in kwargs['extras'].items():
                str_value = ''
                arg = ''
                if isinstance(extra_value, types.IntType):
                    str_value = str(extra_value)
                    arg = '--ei'
                elif isinstance(extra_value, types.BooleanType):
                    str_value = str(extra_value)
                    arg = '--ez'
                else:
                    str_value = str(extra_value)
                    arg = '--es'
                shellcmd.append(arg)
                shellcmd.append(extra_key)
                shellcmd.append(str_value)
                
        if 'flags' in keys:
            shellcmd.append('-f')
            shellcmd.append(str(kwargs['flags']))

        if 'uri' in keys:
            shellcmd.append(kwargs['uri'])
        #sys.stderr.write(str(shellcmd))            
        self.d.server.adb.cmd(*shellcmd).communicate()
        return self

    def instrument(self, **kwargs):
        keys = kwargs.keys()
        shellcmd = ['shell', 'am', 'instrument', '-w', '-r']
        pkgname = kwargs.pop('packagename')
        for k, v in kwargs.items():
            if k and v:
                shellcmd.append('-e')
                shellcmd.append(k)
                shellcmd.append(str(v))
        shellcmd.append(pkgname)
        result = self.d.server.adb.cmd(*shellcmd).communicate()
        return result

    def TODOinstallPackage(self, **kwargs):
        pass

    def TODOremovePackage(self, **kwargs):
        pass

    def press(self, keyname, waittime=1):
        #hard, soft key: home,back,up,down,right,left,center,menu,power or ANDROID_KEYEVENT
        self.d.press(keyname)
        time.sleep(waittime)
        return self

    def click(self, x, y, waittime=1):
        self.d.click(x, y)
        time.sleep(waittime)
        return self

    def click_image(self, imagename, waittime=1, threshold=0.01):
        '''
        if the wanted image found on current screen click it.
        if the wanted image not found raise exception and set test to be failure.
        '''
        expect_image_path = os.path.join(configer['right_dir_path'], imagename)
        assert os.path.exists(expect_image_path), 'the local expected image %s not found!' % imagename
        current_image_path = os.path.join(configer['report_dir_path'], imagename)
        self.d.screenshot(current_image_path)
        assert os.path.exists(current_image_path), 'fetch current screen shot image %s failed!' % imagename
        pos = getMatchedCenterOffset(expect_image_path, current_image_path, threshold)
        assert pos, 'Fail Reason: The wanted image \'%s\' not found on screen!' % imagename
        self.d.click(pos[0], pos[1])
        time.sleep(waittime)
        return self

    def swipe(self, sx, sy, ex, ey, steps=100, waittime=1):
        self.d.swipe(sx, sy, ex, ey, steps)
        time.sleep(waittime)
        return self

    def drag(self, sx, sy, ex, ey, steps=100, waittime=1):
        self.d.drag(sx, sy, ex, ey, steps)
        time.sleep(waittime)
        return self

    #inspect
    def exists(self, **kwargs):
        '''
        if the expected component exists on current screen layout return true else return false.
        '''
        return self.d.exists(**kwargs)

    #device snapshot
    def screenshot(self, filename, waittime=1):
        path = os.path.join(configer['report_dir_path'], filename)
        self.d.screenshot(path)
        return self

    def expect(self, imagename, interval=2, timeout=4, threshold=0.01, msg=''):
        '''
        if the expected image found on current screen return self 
        else raise exception. set test to be failure.
        '''
        expect_image_path = os.path.join(configer['right_dir_path'], imagename)
        assert os.path.exists(expect_image_path)
        current_image_path = os.path.join(configer['report_dir_path'], imagename)
        begin = time.time()
        while (time.time() - begin < timeout):
            self.d.screenshot(current_image_path)
            if isMatch(expect_image_path , current_image_path , threshold):
                return self
            time.sleep(interval)
        name, ext = os.path.splitext(os.path.basename(imagename))
        shutil.copyfile(expect_image_path, os.path.join(configer['report_dir_path'], '%s%s%s' % (name, '_expect', ext)))
        reason = msg if not msg else 'Fail Reason: Image \'%s\' not found on screen!' % imagename
        assert False, reason

    def find(self, imagename, interval=2, timeout=4, threshold=0.01):
        '''
        if the expected image found on current screen return true else return false
        '''
        expect_image_path = os.path.join(configer['right_dir_path'], imagename)
        assert os.path.exists(expect_image_path)
        current_image_path = os.path.join(configer['report_dir_path'], imagename)
        begin = time.time()
        isExists = False
        while (time.time() - begin < timeout):
            time.sleep(interval)
            self.d.screenshot(current_image_path)
            isExists = isMatch(expect_image_path , current_image_path , threshold)
            if not isExists:
                time.sleep(interval)
                continue
        return isExists

device = AndroidDevice()





































