# This file is part of [MFEK/sfdutf7.py](https://github.com/MFEK/sfdutf7.py);
# see __init__.py for reuse information.

from typing import Iterator

import warnings

# Removes all C0/C1 controls except tab (U+0009) and CRLF (U+000D U+000A). Cf.:
# <https://github.com/tenderlove/libxml2/blob/ecb5d5a/include/libxml/chvalid.h#L108>
_xmlIsChar_ch = lambda c: (
    ((0x9 <= (c)) and ((c) <= 0xA)) or ((c) == 0xD) or (0x20 <= (c))
)


def _str_for_str(ch: str) -> str:
    c = ord(ch)

    if c == 0x0B:  # VERTICAL TABULATION
        warnings.warn("Replaced 0x0B with newline; suspected FontForge bug?")
        ret = ord("\n")
    elif not _xmlIsChar_ch(c):
        warnings.warn(f"Replaced 0x0B with newline in string {s}!")
        ret = ord("�")
    else:
        ret = c

    return chr(ret)


def _force_text_validity(s: str) -> Iterator[str]:
    for ch in s:
        for cp in ch:
            yield _str_for_str(cp)


def force_text(s: str) -> str:
    return "".join(_force_text_validity(s))
