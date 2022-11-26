import usb_cdc
import storage

usb_cdc.enable(data=True)
storage.remount("/", False)