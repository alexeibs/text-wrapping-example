import argparse
import sys


MAX_WEIGHT = 1e100


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


class Line:
    def __init__(self, words, start, end, width):
        if start > end:
            raise Exception(f"invalid Line range: {start}, {end}")
        self.words = words
        self.start = start
        self.end = end
        self.width = width

    def calc_weight(self, column_width):
        return calc_line_weight(self.width, column_width, self.end == len(self.words))

    def expand_right(self):
        if self.end < len(self.words):
            self.width += len(self.words[self.end])
            if self.end > self.start:
                self.width += 1 # put a space in between
            self.end += 1

    def copy(self):
        return Line(self.words, self.start, self.end, self.width)

    def empty(self):
        return self.start >= self.end

    def format(self, column_width):
        return format_line(self.words, range(self.start, self.end), self.width, column_width)


class SuffixSolution:
    def __init__(self, first_line, weight, next_suffix):
        self.first_line = first_line
        self.weight = weight
        self.next_suffix = next_suffix


def wrap_text(text, column_width):
    words = split_text(text, column_width)
    return wrap_words(words, column_width)


def wrap_words(words, column_width):
    n_words = len(words)
    suffixes = [None] * (n_words + 1)
    suffixes[n_words] = SuffixSolution(Line(words, n_words, n_words, 0), 0, None)
    for i in range(n_words - 1, -1, -1):
        line = Line(words, i, i + 1, len(words[i]))
        best_weight = line.calc_weight(column_width) + suffixes[line.end].weight
        best_line = line.copy()

        for _ in range(i + 2, n_words + 1):
            line.expand_right()
            if line.width > column_width:
                break
            weight = line.calc_weight(column_width) + suffixes[line.end].weight
            if weight < best_weight:
                best_line = line.copy()
                best_weight = weight

        suffixes[i] = SuffixSolution(best_line, best_weight, suffixes[best_line.end])

    lines = []
    suffix = suffixes[0]
    while not suffix.first_line.empty():
        lines.append(suffix.first_line.format(column_width))
        suffix = suffix.next_suffix

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
                        help='path to input file (stdin by default)')
    parser.add_argument('--width', dest='column_width', action='store',
                        type=int, default=80, help='text column width (80 by default)')
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
