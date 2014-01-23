devicewrapper
=============

a wrapper of Python for android uiautomator-client. provides more event inject and inspect way.

### Install
    sudo pip install devicewrapper

### Dependency
    sudo apt-get install python-opencv
    sudo apt-get install python-numpy
    
### Basic API Usages
   ```
   from devicewrapper.android import device as d
   d.info
   d.wakeup()
   d.start_activity(action='android.intent.action.DIAL', data='tel:xxxx', flags=0x04000000)
   d.find('phone_launch_success.png')
   d.click(100, 200)
   d.click('DPAD_NUMBER_1.png')
   d.click('DPAD_NUMBER_1.png', rotation=90)
   d.exists(text='string_value_of_screen_layout_component_text_attribute')
   d.expect('phone_launch_success.png')
   d(text='Settings').click()
   ```

