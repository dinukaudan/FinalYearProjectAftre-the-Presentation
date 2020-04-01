#!/usr/bin/env python
import codecs
import os.path

########################################
# for counting code lines
########################################
def count_lines(path, extensions):
    comment_symbol = "//"
    if not extensions:
        print('Please pass at least one file extension as an argument.')
        quit()
    files_to_check = []
    for root, _, files in os.walk(path):
        for f in files:
            fullpath = os.path.join(root, f)
            if '.git' not in fullpath:
                for extension in extensions:
                    if fullpath.endswith(extension):
                        files_to_check.append(fullpath)
    if not files_to_check:
        print('No files found.')
        quit()
    line_count = 0
    total_blank_line_count = 0
    total_comment_line_count = 0
    for fileToCheck in files_to_check:
        with codecs.open(fileToCheck, encoding='utf-8', errors='ignore') as f:

            file_line_count = 0
            file_blank_line_count = 0
            file_comment_line_count = 0

            for line in f:
                line_count += 1
                file_line_count += 1

                line_without_whitespace = line.strip()
                if not line_without_whitespace:
                    total_blank_line_count += 1
                    file_blank_line_count += 1
                elif line_without_whitespace.startswith(comment_symbol):
                    total_comment_line_count += 1
                    file_comment_line_count += 1
    total_code_line_count = line_count - total_blank_line_count - total_comment_line_count
    return {
        'blankLines': total_blank_line_count,
        'codeLines': total_code_line_count,
    }
