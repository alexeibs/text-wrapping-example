import sys


def wrap_text(text, column_width):
    return [text]


def parse_args():
    return {'column_width': 80}


def main():
    args = parse_args()
    for paragraph in sys.stdin:
        lines = wrap_text(paragraph.strip(), args['column_width'])
        for line in lines:
            sys.stdout.write(line)
            sys.stdout.write('\n')


if __name__ == "__main__":
    main()
