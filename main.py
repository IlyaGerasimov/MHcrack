import argparse
import os
import program_config
from encrypt import encrypt_inter, encrypt_cli
from decrypt import decrypt_hack, decrypt_pure
from gen import gen


def parse_init():
    parser = argparse.ArgumentParser(description='El-Gamal.')
    parser.add_argument(
        '-g', '--generate',
        action='store_true',
        help='Mode for generation process.'
    )
    parser.add_argument(
        '-n',
        nargs='?',
        default=None,
        help="Difficulty parameter: vector size. Required if there is '-g' flag."
    )
    parser.add_argument(
        '-b',
        nargs='?',
        default=None,
        help="Difficulty parameter: minimal length. Required if there is '-g' flag."
    )
    parser.add_argument(
        '-e', '--encrypt',
        action='store_true',
        help='Mode for encryption process.'
    )
    parser.add_argument(
        '-f', '--file',
        nargs="?",
        type=argparse.FileType('r'),

        help="File with public key. Required if there is '-e' and no '-f' flags or '-d' flag."
    )
    parser.add_argument(
        '-c', '--ciphertext',
        nargs='?',
        default=None,
        help="Encrypted message. Required if there is '-d' flag."
    )
    parser.add_argument(
        '-d', '--decrypt',
        action='store_true',
        help='Mode for decryption (hack) mode.'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Establish interactive mode for encryption.'
    )
    parser.add_argument(
        '-m', '--message',
        nargs='?',
        type=str,
        default=None,
        help="Message for encryption. Required if there is '-e' and no '-m' flag."
    )
    args = parser.parse_args()
    if args.generate:
        if args.n and args.b:
            return args, 1
        else:
            exit("There is '-g' flag but no parameters.")
    if args.encrypt:
        if args.file and args.message:
            return args, 2
        elif args.interactive:
            return args, 2
        else:
            exit("There is '-e' flag but no parameters.")
    if args.decrypt:
        if args.file and args.ciphertext:
            return args, 3
        else:
            exit("There is '-d' flag but no parameters.")
    exit("There is no mode flag.")


if __name__ == '__main__':
    args, mode = parse_init()
    if mode == 1:
        gen(int(args.n), int(args.b))
    elif mode == 2:
        if args.interactive:
            encrypt_inter()
        else:
            encrypt_cli(args.file, args.message)
    else:
        decrypt_hack(args.ciphertext, args.file)
