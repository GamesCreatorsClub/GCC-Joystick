# GCC-Joystick
Raspberry Pi Zero W as Bluetooth Joystick

## Configuration

By default, the `bluetoothd` service starts a plugin called `input`, that binds to the L2CAP ports (17 and 19) used by the joystick service. This would cause connections to fail silently. To fix this, the `input` plugin needs to be disabled. Edit `/lib/systemd/system/bluetooth.service` and change the `ExecStart` line:

    ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=input

Then restart the service:

    systemctl daemon-reload
    service bluetooth restart

(Older versions of `bluetoothd` also supported a `DisablePlugins` in `/etc/bluetooth/main.conf`, but this doesn’t work any more. Confusingly, there is also `/etc/init.d/bluetooth`, but changing options there doesn’t seem to have any effect.)
