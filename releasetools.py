#
# Copyright (C) 2020-2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

import common
import re

def FullOTA_InstallEnd(info):
    OTA_InstallEnd(info)

def IncrementalOTA_InstallEnd(info):
    OTA_InstallEnd(info)

def AddImage(info, basename, dest):
    name = basename
    data = info.input_zip.read("IMAGES/" + basename)
    common.ZipWriteStr(info.output_zip, name, data)
    info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))
    info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def OTA_InstallEnd(info):
    PatchVendor(info)
    AddImage(info, "dtbo.img", "/dev/block/bootdevice/by-name/dtbo")
    AddImage(info, "vbmeta.img", "/dev/block/bootdevice/by-name/vbmeta")
    AddImage(info, "vbmeta_system.img", "/dev/block/bootdevice/by-name/vbmeta_system")

def PatchVendor(info):
  info.script.Print("Patching vendor init scripts...")
  info.script.AppendExtra('mount("ext4", "EMMC", "/dev/block/platform/bootdevice/by-name/vendor", "/vendor");')
  info.script.AppendExtra('run_program("/sbin/sed", "-i", "s/wait,check,formattable,quota,resize/latemount,wait,check,formattable,quota/", "/vendor/etc/fstab.mt6877");')
  info.script.AppendExtra('run_program("/sbin/sed", "-i", "s/fstab.mt6877$/fstab.mt6785 --early\\n    mount_all \/vendor\/etc\/fstab.mt6785 --late/", "/vendor/etc/init/hw/init.mt6785.rc");')
  info.script.AppendExtra('unmount("/vendor");')
