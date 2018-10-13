#!/usr/bin/env python3
# pylint: disable=wildcard-import, unused-wildcard-import, invalid-name

"""Tiny vulkan wrapper"""

from ctypes import *

VkStructureType = c_uint32  # enum (unsigned, size == 4)
VK_STRUCTURE_TYPE_APPLICATION_INFO = 0
VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1

VkInstanceCreateFlags = c_uint32  # enum (unsigned, size == 4)

VkInstance = c_void_p  # handle (struct ptr)


def vk_make_version(major, minor, patch):
    return c_uint32((major << 22) | (minor << 12) | patch)


def decode_vk_version(version):
    major = version.value >> 22
    minor = (version.value >> 12) & 0x3ff
    patch = version.value & 0xfff
    return major, minor, patch


class VkApplicationInfo(Structure):

    # pylint: disable=too-few-public-methods

    _fields_ = [('sType', VkStructureType),
                ('pNext', c_void_p),
                ('pApplicationName', c_char_p),
                ('applicationVersion', c_uint32),
                ('pEngineName', c_char_p),
                ('engineVersion', c_uint32),
                ('apiVersion', c_uint32)]

    def __init__(self):
        super().__init__()
        self.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO
        self.pApplicationName = b"vkinfo"
        self.applicationVersion = vk_make_version(0, 1, 0)
        self.apiVersion = vk_make_version(1, 0, 0)


class VkInstanceCreateInfo(Structure):

    # pylint: disable=too-few-public-methods

    _fields_ = [('sType', VkStructureType),
                ('pNext', c_void_p),
                ('flags', VkInstanceCreateFlags),
                ('pApplicationInfo', POINTER(VkApplicationInfo)),
                ('enabledLayerCount', c_uint32),
                ('ppEnabledLayerNames', c_char_p),
                ('enabledExtensionCount', c_uint32),
                ('ppEnabledExtensionNames', c_char_p)]

    def __init__(self, app_info):
        super().__init__()
        self.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        self.pApplicationInfo = pointer(app_info)


def main():
    vulkan = CDLL("libvulkan.so.1")

    version = c_uint32(0)
    vulkan.vkEnumerateInstanceVersion(byref(version))
    print(decode_vk_version(version))

    app_info = VkApplicationInfo()
    create_info = VkInstanceCreateInfo(app_info)

    instance = VkInstance()
    err = vulkan.vkCreateInstance(byref(create_info), 0, byref(instance))
    print(err)

    dev_count = c_uint32(0)
    err = vulkan.vkEnumeratePhysicalDevices(instance, byref(dev_count), 0)
    print(err, dev_count.value)

    vulkan.vkDestroyInstance(instance, 0)


if __name__ == "__main__":
    main()
