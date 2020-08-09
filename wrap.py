import argparse
import sys


MAX_WEIGHT = 1000000000


def calc_line_width(words, line_range):
    if not line_range:
        return 0

    width = len(line_range) - 1 # necessary spaces
    for i in line_range:
        width += len(words[i])
    return width


def calc_line_weight(width, column_width, is_last_line):
    if width > column_width:
        return MAX_WEIGHT

    if is_last_line:
        # ignore extra space in the last line
        return 0

    extra_space = column_width - width
    return extra_space * extra_space * extra_space


def format_line(words, line_range, width, column_width):
    if not words:
        return ''

    extra_space = column_width - width
    if extra_space <= 0 or line_range.stop == len(words):
        return ' '.join([words[i] for i in line_range])

    tokens = [words[line_range[0]]]
    for i in range(1, len(line_range)):
        if extra_space <= 0:
            tokens.append(' ')
        else:
            # ensure spaces are distributed equally between words
            sp_start = extra_space * (i - 1) // (len(line_range) - 1)
            sp_end = extra_space * i // (len(line_range) - 1)
            tokens.append(' ' * (sp_end - sp_start + 1))
        tokens.append(words[line_range[i]])
    return ''.join(tokens)


class SuffixSolution:
    def __init__(self, words, first_line_range, width, weight, next_line_suffix):
        self.words = words
        self.first_line_width = width
        self.first_line_range = first_line_range
        self.suffix_weight = weight
        self.next_line_suffix = next_line_suffix

    def weight(self):
        return self.suffix_weight

    def first_line(self, column_width):
        return format_line(self.words, self.first_line_range, self.first_line_width, column_width)

    def next(self):
        return self.next_line_suffix

    def empty(self):
        return len(self.first_line_range) == 0


def wrap_text(text, column_width):
    words = split_text(text, column_width)
    return wrap_words(words, column_width)


def wrap_words(words, column_width):
    n_words = len(words)
    suffixes = [None] * (n_words + 1)
    suffixes[n_words] = SuffixSolution(words, range(n_words, n_words), 0, 0, None)
    for i in range(n_words - 1, -1, -1):
        best = i + 1
        line_width = calc_line_width(words, range(i, best))
        weight = calc_line_weight(line_width, column_width, best == n_words)
        best_weight = weight + suffixes[best].weight()
        for j in range(i + 2, n_words + 1):
            width = calc_line_width(words, range(i, j))
            weight = calc_line_weight(width, column_width, j == n_words)
            if width > column_width:
                break
            new_weight = weight + suffixes[j].weight()
            if new_weight < best_weight:
                best = j
                best_weight = new_weight
                line_width = width

        suffixes[i] = SuffixSolution(words, range(i, best), line_width, best_weight, suffixes[best])

    lines = []
    suffix = suffixes[0]
    while not suffix.empty():
        lines.append(suffix.first_line(column_width))
        suffix = suffix.next()

    return lines


def split_text(text, column_width):
    words = []
    for word in text.split():
        if len(word) > column_width:
            words += split_big_word(word, column_width)
        else:
            words.append(word)
    return words if words else ['']


def split_big_word(word, width_limit):
    result = []
    start = 0
    while start + width_limit < len(word):
        result.append(word[start : start + width_limit])
        start += width_limit

    if start < len(word):
        result.append(word[start:])

    return result


def parse_args():
    parser = argparse.ArgumentParser(description='Wrapping text using DP')
    parser.add_argument('--input', dest='input_path', action='store',
                        help='path to input file')
    parser.add_argument('--width', dest='column_width', action='store',
                        type=int, default=80, help='text column width')
    return parser.parse_args()


def main():
    args = parse_args()
    infile = sys.stdin if not args.input_path else open(args.input_path)
    for paragraph in infile:
        lines = wrap_text(paragraph.strip(), args.column_width)
        for line in lines:
            sys.stdout.write(line)
            sys.stdout.write('\n')


if __name__ == "__main__":
    main()
