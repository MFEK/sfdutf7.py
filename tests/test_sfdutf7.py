import ctypes
import ctypes.util
from ctypes import (
    POINTER,
    Structure,
    py_object,
    pythonapi,
    c_void_p,
    c_int,
    c_char_p,
    pointer,
)
import logging
import os

import sfdutf7

libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library("c"))
libfontforge = ctypes.cdll.LoadLibrary(ctypes.util.find_library("fontforge"))


class FILE(Structure):
    pass


fdopen = libc.fdopen
fdopen.restype = POINTER(FILE)
fdopen.argtypes = [c_int, c_char_p]

SFDDumpUTF7Str = libfontforge.SFDDumpUTF7Str
SFDDumpUTF7Str.restype = c_void_p
SFDDumpUTF7Str.argtypes = [POINTER(FILE), c_char_p]

SFDReadUTF7Str = libfontforge.SFDReadUTF7Str
SFDReadUTF7Str.restype = c_char_p
SFDReadUTF7Str.argtypes = [POINTER(FILE)]

def libfontforge_sfdutf7decode(s: bytes) -> str:
    filename = '/tmp/sfdutf7_SFDDumpUTF7StrOUT'
    fp = open(filename, 'wb+')
    fp.write(b'"')
    fp.write(s)
    fp.write(b'"')
    fp.close()
    fp = open(filename, 'rb')
    c_file = fdopen(c_int(fp.fileno()), c_char_p(fp.mode.encode('ascii')))
    buffer = SFDReadUTF7Str(c_file)
    libc.fclose(c_file)
    logging.debug("libfontforge_sfdutf7decode buffer: {}".format(buffer.decode('utf-8')))
    return buffer.decode('utf-8')

def libfontforge_sfdutf7encode(s: str) -> bytes:
    filename = '/tmp/sfdutf7_SFDDumpUTF7StrOUT'
    fp = open(filename, 'wb+')
    c_file = fdopen(c_int(fp.fileno()), c_char_p(fp.mode.encode('ascii')))

    SFDDumpUTF7Str(c_file, c_char_p(s.encode('utf-8')))
    libc.fclose(c_file)
    with open(filename, 'rb') as f:
        ret = f.read()
    os.unlink(filename)
    logging.debug("libfontforge_sfdutf7encode buffer: {}".format(ret.decode('utf-8')))
    return ret

test_strings = [
    '"',
    '""',
    '"\n',
    '" ',
    '"A',
    '日本go語'
]

def test_decode():
    for to_encode in test_strings:
        encoded = libfontforge_sfdutf7encode(to_encode)[1:-1]
        decoded = sfdutf7.decode(encoded)
        assert to_encode == decoded


def test_encode():
    for to_encode in test_strings:
        encoded = sfdutf7.encode(to_encode)
        decoded = libfontforge_sfdutf7decode(encoded)
        assert to_encode == decoded
