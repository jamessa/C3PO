#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.
#
# Localize.py - Incremental localization on XCode projects
# João Moreno 2009
# http://joaomoreno.com/

from codecs import open
from re import compile
from copy import copy
import io
import os

re_translation = compile(r'^"(.+)" = "(.+)";$')
re_comment_single = compile(r'^/\*.*\*/$')
re_comment_start = compile(r'^/\*.*$')
re_comment_end = compile(r'^.*\*/$')
re_widecamelcase = compile(r'(?x)( [A-Z](\S+)([A-Z](\S*))+ | ([A-Z_][A-Z_]+) )')  # LogIn or LOG_IN

useUTF8 = False


def usage():
    print u"""
Usage: Localize.py pathToYourCocoaProject
try `localize.py --help' for more information.
"""


class LocalizedString():
    def __init__(self, comments, translation):
        self.comments, self.translation = comments, translation
        self.key, self.value = re_translation.match(self.translation).groups()

    def __unicode__(self):
        return u'%s%s\n' % (u''.join(self.comments), self.translation)


class LocalizedFile():
    def __init__(self, fname=None, auto_read=False):
        self.fname = fname
        self.strings = []
        self.strings_d = {}

        if auto_read:
            self.read_from_file(fname)

    def read_from_file(self, fname=None):
        fname = self.fname if fname == None else fname
        try:
            f = open(fname, encoding='utf_16', mode='r')
        except:
            print 'File %s does not exist.' % fname
            exit(-1)

        line = f.readline()
        while line:
            comments = [line]

            if not re_comment_single.match(line):
                while line and not re_comment_end.match(line):
                    line = f.readline()
                    comments.append(line)

            line = f.readline()
            if line and re_translation.match(line):
                translation = line
            else:
                raise Exception('invalid file')

            line = f.readline()
            while line and line == u'\n':
                line = f.readline()

            string = LocalizedString(comments, translation)
            self.strings.append(string)
            self.strings_d[string.key] = string

        f.close()

    def save_to_file(self, fname=None):
        fname = self.fname if fname == None else fname
        try:
            f = open(fname, encoding='utf_16', mode='w')

        except:
            print 'Couldn\'t open file %s.' % fname
            exit(-1)

        for string in self.strings:
            f.write(string.__unicode__())

        f.close()

    def merge_with(self, new):
        merged = LocalizedFile()

        for string in new.strings:
            if string.key in self.strings_d:
                new_string = copy(self.strings_d[string.key])
                new_string.comments = string.comments
                string = new_string

            merged.strings.append(string)
            merged.strings_d[string.key] = string

        return merged


def merge(merged_fname, old_fname, new_fname):
    try:
        old = LocalizedFile(old_fname, auto_read=True)
        new = LocalizedFile(new_fname, auto_read=True)
    except:
        print 'Error: input files have invalid format.'

    merged = old.merge_with(new)

    merged.save_to_file(merged_fname)

STRINGS_FILE = 'Localizable.strings'


# use ibtool to extract localizable strings from ib files
def export_xibs(language):
    # XIBs
    localization = open(language + os.path.sep + 'xib.strings.new', encoding='utf_16', mode='w+')

    ibs = [name for name in os.listdir(os.getcwd()) if name.endswith('.xib') and not os.path.isdir(name)]

    for ib in ibs:
        ib_strings = "en.lproj/" + ib + ".strings.new"

        # extract only if modified
        print 'ibtool --export-strings-file "%s" "%s"' % (ib_strings, ib)
        # run ibtool only once per modification
        if not os.path.isfile(ib_strings) or (os.stat(ib).st_mtime > os.stat(ib_strings).st_mtime):
            os.system('ibtool --export-strings-file "%s" "%s"' % (ib_strings, ib))
            os.system('touch %s' % ib_strings)

        fin = open(ib_strings, encoding='utf_16', mode='r')

        line = fin.readline()
        comments = []
        while line:
            translate = re_translation.match(line)
            if translate:
                wrong_key, key = translate.groups()
                if re_widecamelcase.match(key) and not key.count(' '):
                    for comment in comments:
                        localization.write(comment)
                    localization.write(u'"%s" = "%s";' % (key, key))
                    localization.write("\n")
                comments = []
            else:
                comments.append(line)
            line = fin.readline()
    localization.close()
    return localization.name


def concat(file1, file2):
    io.open(file1, encoding='utf-16', mode='a').write(open(file2, encoding='utf-16').read())


def localize(path):
    # init phase the new
    start_with = 'en'

    language = start_with + '.lproj'
    original = merged = language + os.path.sep + STRINGS_FILE
    old = original + '.old'
    new = original + '.new'

    if os.path.isfile(original):
        os.rename(original, old)
        os.system('genstrings -q -o "%s" `find . -name "*.m"`' % language)
        os.rename(original, new)
        concat(new, export_xibs(language))
    else:
        os.system('genstrings -q -o "%s" `find . -name "*.m"`' % language)

    merge(merged, old, new)

    languages = [name for name in os.listdir(path) if name.endswith('.lproj') and os.path.isdir(name) and not name.startswith('en.')]
    for language in languages:
        original = merged = language + os.path.sep + STRINGS_FILE
        old = original + '.old'

        if os.path.isfile(original):
            os.rename(original, old)

        merge(merged, old, new)

if __name__ == '__main__':
    localize(os.getcwd())
