import argparse
import sys


def split_big_word(word, width_limit):
    result = []
    start = 0
    while start + width_limit < len(word):
        result.append(word[start : start + width_limit])
        start += width_limit

    if start < len(word):
        result.append(word[start:])

    return result


def wrap_text(text, column_width):
    words = []
    for word in text.split():
        if len(word) > column_width:
            words += split_big_word(word, column_width)
        else:
            words.append(word)
    return words if words else ['']


def parse_args():
    parser = argparse.ArgumentParser(description='Wrapping text using DP')
    parser.add_argument('--width', dest='column_width', action='store',
                        default=80, help='text column width')
    return parser.parse_args()


def main():
    args = parse_args()
    for paragraph in sys.stdin:
        lines = wrap_text(paragraph.strip(), args.column_width)
        for line in lines:
            sys.stdout.write(line)
            sys.stdout.write('\n')


if __name__ == "__main__":
    main()
