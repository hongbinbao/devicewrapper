devicewrapper
=============

device wrapper of python uiautomator(android) and image comparison

### Basic API Usages
   ```
   from devicewrapper.android import device as d
   d.info()
   d.wakeup()
   d.start_activity(action='android.intent.action.DIAL', data='tel:xxxx', flags=0x04000000)
   d.find('phone_launch_success.png')
   d.exists(text='string_value_of_screen_layout_component_text_attribute')
   d.expect('phone_launch_success.png')
   ```
