#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file contains two main methods used to encode and decode "SFD" UTF-7
# string, based heavily on functions written for the IMAPClient project.
#
# The IMAPClient library cannot be used directly due to these FontForge quirks:
#     * the non-use of `,` instead of `/` which was a change in RFC 3501;
#     * the non-use of `&` instead of `+` which was also a change in RFC 3501;
#     * the mandatory termination with `A`/`AA` (0x0) to make the number of
#       bytes even;
#     * the mandatory handling of both string terminated in `A` and `-`;
#     * the mandatory encoding of `"`.
#
# Copyright (c) 2014–2022
# sfdnormalize: Fredrick R. Brennan (@ctrlcctrlv)
# IMAPClient¹: Menno Finlay-Smits (@mjs), Carson Ip (GitHub @carsonip), Mathieu
#              Agopian (@magopian), John Villalovos (@JohnVillalovos)
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Menno Smits nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL MENNO SMITS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ¹ The version of IMAPClient this is based on is
#   6e6ec34b0e71975134d9492add22361ce4beb2a0:
#   <https://github.com/mjs/imapclient/blob/6e6ec34b0e71975134d9492add22361ce4beb2a0/imapclient/imap_utf7.py>.

import binascii
import string

PLUS_ORD = ord(b'+')
DASH_ORD = ord(b'-')
CAP_A_ORD = ord(b'A')
QUOT_ORD = ord(b'"')
EQUALS_ORD = ord(b'=')
MODIFIED_B64 = (string.ascii_lowercase + string.ascii_uppercase + string.digits).encode('ascii') + b'/'

def encode(s: str, quote=False) -> bytes:
    res = bytearray()
    b64_buffer = list()

    def consume_b64_buffer(buf):
        """
        Consume the buffer by encoding it into a "modified base 64" (
        representation and surround it with shift characters + and -
        """
        if buf:
            # FontForge SFD extension: null (0x00) bytes are used to end UTF7
            # buffer. In IMAP, the last (shift) character would be "-" here.
            ext = bytearray(b'+' + _base64_utf7_encode(buf))
            # FontForge quirk: must be even len
            if ext[-2] == EQUALS_ORD:
                ext = ext[:-1]
            if ext[-1] == EQUALS_ORD:
                ext[-1] = CAP_A_ORD
                ext = ext + b'-'
            res.extend(bytes(ext))
            del buf[:]

    for c in s:
        # printable ascii case should not be modified
        o = ord(c)
        # (FontForge SFD exception:
        #                        " is always encoded)
        if 0x20 <= o <= 0x7E and o != QUOT_ORD:
            consume_b64_buffer(b64_buffer)
            # Special case: + is used as shift character so we need to escape
            # it in ASCII
            if o == PLUS_ORD: # 0x2B = +
                res.extend(b"+-")
            else:
                res.append(o)

        # Bufferize characters that will be encoded in base64 and append them
        # later in the result, when iterating over ASCII character or the end
        # of string
        else:
            b64_buffer.append(c)

    # Consume the remaining buffer if the string finish with non-ASCII
    # characters
    consume_b64_buffer(b64_buffer)

    if quote:
        res.insert(0, QUOT_ORD)
        res.append(QUOT_ORD)

    return bytes(res)

def decode(s: bytes, quote=False) -> str:
    if quote and len(s) >= 2 and s[0] == QUOT_ORD and s[-1] == QUOT_ORD:
        s = s[1:-1]

    res = []
    # Store b64 substring that will be decoded once stepping on end shift char
    b64_buffer = bytearray()
    for c in s:
        if c == PLUS_ORD:
            b64_buffer.append(c)
        # End shift char → append the decoded buffer to the result and reset it
        elif (c == DASH_ORD or c not in MODIFIED_B64) and b64_buffer:
            # Special case: +- represents «+» escaped
            if len(b64_buffer) == 1:
                res.append("+")
            else:
                res.append(_base64_utf7_decode(b64_buffer[1:]))
            b64_buffer = bytearray()
            if c != DASH_ORD:
                res.append(chr(c))
        # Shift character w/o anything in buffer → starts storing b64 substr
        # Or still buffering between the shift character and the shift back to ASCII
        elif c in MODIFIED_B64 and (len(b64_buffer) > 0 or b64_buffer == [PLUS_ORD]):
            b64_buffer.append(c)
        # No buffer initialized yet, should be an ASCII printable char
        else:
            res.append(chr(c))

    # Decode the remaining buffer, if any
    if b64_buffer:
        res.append(_base64_utf7_decode(b64_buffer[1:]))

    return "".join(res)

def _base64_utf7_encode(buffer: str) -> bytes:
    s = "".join(buffer).encode("utf-16be")
    return binascii.b2a_base64(s, newline=False)

def _base64_utf7_decode(s: bytes) -> str:
    s = bytearray(s)
    # Cut off FontForge's final `A` or `AA` because it's invalid UTF-7.
    # (This quirk is because FontForge wrongly encodes the unneeded 0's.)
    if len(s) >= 2 and len(s) % 2 == 0 and s[-2] == CAP_A_ORD and s[-1] == CAP_A_ORD:
        s = s[:-2]
    elif s[-1] == CAP_A_ORD:
        s = s[:-1]
    if not s[-1] == DASH_ORD:
        s = s + b'-'
    s_utf7 = b'+' + s
    return s_utf7.decode("utf-7")
