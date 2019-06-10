#!/usr/bin/env python3
# pylint: disable=wildcard-import, unused-wildcard-import, invalid-name


import sys
from ctypes import *

# https://www.khronos.org/registry/OpenGL/extensions/MESA/GLX_MESA_query_renderer.txt
GLX_RENDERER_VENDOR_ID_MESA = 0x8183
GLX_RENDERER_DEVICE_ID_MESA = 0x8184
GLX_RENDERER_VERSION_MESA = 0x8185
GLX_RENDERER_ACCELERATED_MESA = 0x8186
GLX_RENDERER_VIDEO_MEMORY_MESA = 0x8187
GLX_RENDERER_UNIFIED_MEMORY_ARCHITECTURE_MESA = 0x8188
GLX_RENDERER_PREFERRED_PROFILE_MESA = 0x8189
GLX_RENDERER_OPENGL_CORE_PROFILE_VERSION_MESA = 0x818A
GLX_RENDERER_OPENGL_COMPATIBILITY_PROFILE_VERSION_MESA = 0x818B
GLX_RENDERER_OPENGL_ES_PROFILE_VERSION_MESA = 0x818C
GLX_RENDERER_OPENGL_ES2_PROFILE_VERSION_MESA = 0x818D


def main():

    x11 = CDLL("libX11.so.6")

    x11.XOpenDisplay.argtypes = [c_char_p]
    x11.XOpenDisplay.restype = c_void_p

    x11.XDisplayString.argtypes = [c_void_p]
    x11.XDisplayString.restype = c_char_p

    x11.XCloseDisplay.argtypes = [c_void_p]

    dpy_ptr = x11.XOpenDisplay(None)
    if dpy_ptr == None:
        sys.exit(1)

    print('Display:', x11.XDisplayString(dpy_ptr).decode('ascii'))

    gl = CDLL("libGL.so.1")

    gl.glXQueryVersion.argtypes = [c_void_p, POINTER(c_int), POINTER(c_int)]
    gl.glXQueryVersion.restypes = [c_bool]

    glx_version_major = c_int(0)
    glx_version_minor = c_int(0)
    if gl.glXQueryVersion(dpy_ptr, byref(glx_version_major), byref(glx_version_minor)):
       print(f'GLX version: {glx_version_major.value}.{glx_version_minor.value}')

    # GLXContext glXCreateNewContext(Display * dpy,
    #                                GLXFBConfig config,
    #                                int render_type,
    #                                GLXContext share_list,
    #                                Bool direct);
    gl.glXCreateNewContext.argtypes = [c_void_p, , c_int, c_void_p, c_bool]
    gl.glXCreateNewContext.restypes = [c_void_p]

    # Bool glXMakeCurrent(Display * dpy,  GLXDrawable drawable,  GLXContext ctx);
    #gl.glXMakeCurrent.argtypes = [c_void_p, ]
    #gl.glXMakeCurrent.restypes = [c_bool]




    # unsigned int v[3];

    # needs GLX 1.4
    # Bool glXQueryCurrentRendererIntegerMESA(int attribute, unsigned int *value);

    glx_ret_type = c_uint * 3
    gl.glXQueryCurrentRendererIntegerMESA.argtypes = [c_int, POINTER(glx_ret_type)]
    gl.glXQueryCurrentRendererIntegerMESA.restypes = [c_bool]

    # at the moment... NOPE
    # pci_id = glx_ret_type(0, 0, 0)
    # res = gl.glXQueryCurrentRendererIntegerMESA(c_int(0x8183), byref(pci_id))
    # print(f'{res} :: {pci_id[0]}')

    # Bool glXQueryRendererIntegerMESA(Display *dpy, int screen, int renderer,
    #                                     int attribute, unsigned int *value);

    gl.glXQueryRendererIntegerMESA.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(glx_ret_type)]
    gl.glXQueryRendererIntegerMESA.restypes = [c_bool]

    # NOPE
    # value = glx_ret_type(0, 0, 0)
    # ret = gl.glXQueryRendererIntegerMESA(dpy_ptr, 0, 0, GLX_RENDERER_VENDOR_ID_MESA, byref(value))
    # print(f'{ret} :: ')

    x11.XCloseDisplay(dpy_ptr)
    sys.exit(0)


if __name__ == "__main__":
    main()
