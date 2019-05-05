# TODO

- [ ] Clean up main code:
  - [ ] Define what profile, device and services are
  - [ ] Move configuration of path, name and such to default values that can be easily overriden (MY_DEV_NAME, PROFILES_DBUS_PATH, etc)

- [ ] Define Joystick 'interface' - a class that will describe joystick/gamepad device (axes, buttons, etc). Usage should implement it.
- [ ] Make example code to connect Joystick 'interface' with BT service/device/etc...
- [ ] Make above example code to one of the ways to use BT service/device (having main class provided by our package which will be called from
      systemd service and will be 'configured' with user supplied Joystick interface implementation)
- [ ] Make example which will directly use BT service/device instead of going through interface
- [ ] Make 'setup' or 'installation' command/script (python code) which will check/fix systemd/system/bluetooth... service 
      file to exclude 'input' plugin (check for existence of -P or --noplugin switch and add one if not there. Also, such
      utility should know how to add separate service (with user's own or provided main class that uses Joystick interface implementation
- [ ] Organise source code with 'core', 'examples', 'tests' areas
