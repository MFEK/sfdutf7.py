# SFDUTF7 encoder/decoder library

FontForge's Spline Font Databases have a rather unusual encoding called
"UTF-7", but which is incompatible with *either* the common meaning of this
word *or* the IMAP meaning. It is instead its own encoding unrelated to either,
which I have implemented for use in `sfdnormalize` and other projects.

## Tests / source of truth

The ultimate source of truth for this library is the implementation as it
appears in [FontForge](https://github.com/fontforge/fontforge)'s `sfd.c` of
[`SFDDumpUTF7Str`](https://github.com/fontforge/fontforge/blob/18225116959807bcf0276ff07f69a19b0dddfe52/fontforge/sfd.c#L207)
and
[`SFDReadUTF7Str`](https://github.com/fontforge/fontforge/blob/18225116959807bcf0276ff07f69a19b0dddfe52/fontforge/sfd.c#L413).

The function `utf7toutf8_copy` has some involvment as well. There is no spec,
if this library results in a string FontForge can decode transparently (not the
same thing as "exactly the same string FontForge itself would produce"!) my
implementation is right; if it doesn't then it's not, please open a bug! :-)

## License

Copyright (c) 2014–2022

* sfdnormalize: Fredrick R. Brennan (@ctrlcctrlv)
* IMAPClient¹: Menno Finlay-Smits (@mjs), Carson Ip (GitHub @carsonip), Mathieu
Agopian (@magopian), John Villalovos (@JohnVillalovos)

All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of Menno Smits nor the names of its
          contributors may be used to endorse or promote products derived
          from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL MENNO SMITS BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

¹ The version of IMAPClient this is based on is
  6e6ec34b0e71975134d9492add22361ce4beb2a0:
  <https://github.com/mjs/imapclient/blob/6e6ec34b0e71975134d9492add22361ce4beb2a0/imapclient/imap_utf7.py>.
