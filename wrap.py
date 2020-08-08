import argparse
import sys


def wrap_text(text, column_width):
    return [text]


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
