#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import argparse
import os
import re


def create_parser():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-s', '--source',
                         help='the text sample in *.txt \
                         file with UTF-8 encoding')
    _parser.add_argument('-l', '--language', help='language of the text')
    _parser.add_argument('-c', '--clear',
                         help='clear word set for [LANGUAGE]')

    return _parser


def clear_word_set(lang):
    path = '../dictionaries/' + lang
    if os.path.exists(path):
        os.remove(path)
    else:
        print('Word set for language ' + lang + ' not found')


def load_word_set(language):
    path = '../dictionaries/' + language
    if not os.path.exists(path):
        return set()
    file = open(path)
    return file.read().split()


def top_up_word_set(word_set, text):
    for line in text:
        for word in re.split(r'\W*[ |\n]', line):
            word = word.lower()
            if len(word) > 0:
                word_set.add(word)


def save_word_set(word_set, language):
    path = '../dictionaries/' + language
    file = open(path, 'a')
    file.write(' '.join(list(word_set)))


def main(args):
    if args.clear is not None:
        clear_word_set(args.clear)
        return
    if args.source is None:
        print('Expected source')
        return
    if not os.path.exists(args.source):
        print('File ' + args.source + ' not found')
        return
    if args.language is None:
        print('Expected language')
        return
    file = open(args.source)
    text = [line for line in file]
    word_set = load_word_set(args.language)
    prev_len = len(word_set)
    top_up_word_set(word_set, text)
    print(word_set)
    save_word_set(word_set, args.language)
    new_len = len(word_set)
    output = 'Word set for language ' + args.language
    if prev_len == 0:
        output += ' created'
    else:
        output += ' updated'
    if new_len == prev_len:
        output += ', no words added'
    else:
        output += ' with ' + str(new_len - prev_len) + ' new word(s)'
    print(output)


if __name__ == "__main__":
    parser = create_parser()
    main(parser.parse_args(sys.argv[1:]))

