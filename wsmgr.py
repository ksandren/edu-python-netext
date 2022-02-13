#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Word Set Manager

import sys
import argparse
import os
import re

DICT_PATH = 'dictionaries/'


def load_word_set(language):
    path = DICT_PATH + language + '/words.txt'
    if not os.path.exists(path):
        return set()
    file = open(path)
    word_set = set(file.read().split())
    file.close()
    return word_set


def top_up_word_set(word_set, text):
    for line in text:
        for word in re.split(r'\W*[ |\n]', line + '\n'):
            if len(word) > 0 and word[0].islower():
                word_set.add(word)


def save_word_set(word_set, language):
    path = DICT_PATH
    if not os.path.isdir(path):
        os.mkdir(path)
    path += language
    if not os.path.isdir(path):
        os.mkdir(path)
    path += '/words.txt'
    if os.path.isfile(path):
        file = open(path, 'a')
    else:
        file = open(path, 'x')
    file.write('\n'.join(list(word_set)))
    file.close()


def main(args):
    if args.source is None or args.language is None:
        print('Expected source and language (-s [FILENAME] -l [LANG])')
        return
    if not os.path.isfile(args.source):
        print('File ' + args.source + ' not found')
        return
    file = open(args.source)
    text = [line for line in file]
    file.close()
    word_set = load_word_set(args.language)
    prev_len = len(word_set)
    top_up_word_set(word_set, text)
    save_word_set(word_set, args.language)
    new_len = len(word_set)

    if new_len == prev_len:
        print('No words added')
    else:
        print(str(new_len - prev_len) + ' new words added')


def create_parser():
    pars = argparse.ArgumentParser()
    pars.add_argument('-s', '--source',
                      help='the text sample in *.txt \
                         file with UTF-8 encoding')
    pars.add_argument('-l', '--language', help='language of the text')
    pars.add_argument('-c', '--clear',
                      help='clear word set for [LANGUAGE]')
    return pars


if __name__ == "__main__":
    parser = create_parser()
    main(parser.parse_args(sys.argv[1:]))
