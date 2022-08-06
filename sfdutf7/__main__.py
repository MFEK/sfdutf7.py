from sfdutf7 import encode, decode

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Encode/decode SFDUTF7")
    parser.add_argument("-d", "--decode", help="Decode, not encode",
                        action="store_true")
    parser.add_argument("-q", "--quote", help="Quote string for storing in .sfd (or unquote quoted string)",
                        action="store_true")
    args = parser.parse_args()
    inp = sys.stdin.buffer.read()
    if args.decode:
        print(decode(inp, quote=args.quote), end='')
    else:
        print(encode(inp.decode('utf-8'), quote=args.quote).decode('ascii'), end='')

if __name__ == "__main__":
    main()
