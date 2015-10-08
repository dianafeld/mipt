import argparse
import unittest
from collections import Counter, defaultdict
import random


def tokenize(line):
    """Splits string into tokens

    Tokens are alphabetical sequences, numeric sequences, special symbols and whitespaces

    :param line: string to split
    :return: generator with tokens

    """

    token = []
    alpha = False
    numeric = False

    for char in line:
        if not char.isalnum() and char != '\n':
            if token:
                yield ''.join(token)
                token = []
            alpha, numeric = False, False
            yield char

        elif (alpha and char.isalpha()) or (numeric and char.isdigit()):
            token.append(char)

        elif char.isalpha():
            if token:
                yield ''.join(token)
                token = []
            alpha, numeric = True, False
            token.append(char)

        elif char.isnumeric():
            if token:
                yield ''.join(token)
                token = []
            alpha, numeric = False, True
            token.append(char)

    if token:
        yield ''.join(token)


def print_tokens(input_stream, args):
    line = input_stream.readline().strip()

    with open('output.txt', 'w', encoding='utf-8') as output_stream:
        for token in tokenize(line):
            print(token, file=output_stream)


class MarkovChainGenerator:
    """Generates text based on the Markov chain model

    Use calculate_probabilities for training
        generate_text for generating

    """

    def __init__(self, depth):
        self.depth = depth
        self.frequency_table = defaultdict(Counter)

    def calculate_probabilities(self, token_generator):
        """Trains generator

        Creates a table with frequencies

        :param token_generator: an iterable producing tokens

        """

        current_tokens = []
        for token in token_generator:
            for start in range(len(current_tokens) + 1):
                chain = tuple(current_tokens[start:])
                self.frequency_table[chain][token] += 1

            if len(current_tokens) == self.depth:
                current_tokens.pop(0)
            current_tokens.append(token)

    def get_probabilities_table(self):
        probabilities_table = {}

        for chain, token_counter in self.frequency_table.items():
            size = sum(token_counter.values())
            probabilities_table[' '.join(chain)] = [(token, freq / size)
                                                    for token, freq
                                                    in sorted(token_counter.items())]

        return probabilities_table

    def _get_random_token(self, chain):
        token_counter = self.frequency_table[chain]

        if not token_counter:
            return None

        size = sum(token_counter.values())
        rnd = random.randint(0, size - 1)
        current_sum = 0
        for token, freq in token_counter.items():
            current_sum += freq
            if rnd < current_sum:
                return token

    def _get_next_token(self, prev_tokens):
        chain = tuple(prev_tokens)
        return self._get_random_token(chain)

    def _get_starting_token(self):
        new_token = self._get_random_token(tuple())
        while not new_token.isalpha():
            new_token = self._get_random_token(tuple())
        return new_token

    def make_sentence(self, tokens):
        new_tokens = []
        for token in tokens:
            if new_tokens and new_tokens[-1].isalnum() and token.isalnum():
                new_tokens.append(' ')
            elif new_tokens and not new_tokens[-1].isalnum() and token.isalnum():
                if new_tokens[-1] != '-':
                    new_tokens.append(' ')
            new_tokens.append(token)
        return ''.join(new_tokens)

    def generate_text(self, size):
        paragraphs = []
        prev_tokens = []
        is_begin = True

        for i in range(size):
            if is_begin:
                new_token = self._get_starting_token()
                is_begin = False
                prev_tokens.append(new_token)
            else:
                new_token = self._get_next_token(prev_tokens[-self.depth:])

                if new_token is None:
                    if prev_tokens:
                        prev_tokens[0] = prev_tokens[0].title()
                        paragraphs.append(self.make_sentence(prev_tokens))
                        prev_tokens = []
                    is_begin = True
                else:
                    prev_tokens.append(new_token)

        if prev_tokens:
            prev_tokens[0] = prev_tokens[0].title()
            paragraphs.append(self.make_sentence(prev_tokens + ['.']))
        return '\n'.join(paragraphs)


def probabilities(input_stream, args):
    generator = MarkovChainGenerator(args.depth)

    for line in input_stream:
        line = line.strip()
        generator.calculate_probabilities(filter(str.isalpha, tokenize(line)))

    with open('output.txt', 'w', encoding='utf-8') as output_stream:
        for chain, tokens in sorted(generator.get_probabilities_table().items()):
            print(chain, file=output_stream)
            for token, probability in tokens:
                print('  {}: {:.2f}'.format(token, probability), file=output_stream)


def generate(input_stream, args):
    generator = MarkovChainGenerator(args.depth)

    generator.calculate_probabilities(
        filter(lambda x: not x.isspace(), tokenize(input_stream.read())))

    with open('output.txt', 'w', encoding='utf-8') as output_stream:
        print(generator.generate_text(args.size), file=output_stream)


class TestTokenize(unittest.TestCase):

    def test_alpha(self):
        string = 'Hello world'
        tokens = list(tokenize(string))
        self.assertEqual(tokens, ['Hello', ' ', 'world'])

    def test_alpha_digits(self):
        string = 'Hello22 world'
        tokens = list(tokenize(string))
        self.assertEqual(tokens, ['Hello', '22', ' ', 'world'])

    def test_special_symbols(self):
        string = 'Hello, world!'
        tokens = list(tokenize(string))
        self.assertEqual(tokens, ['Hello', ',', ' ', 'world', '!'])


class TestProbabilities(unittest.TestCase):

    def test_one_token(self):
        generator = MarkovChainGenerator(1)
        tokens = ['Hello']
        generator.calculate_probabilities(tokens)
        probabilities_table = generator.get_probabilities_table()
        self.assertEqual(probabilities_table,
                         {'': [('Hello', 1.0)]})

    def test_two_tokens(self):
        generator = MarkovChainGenerator(1)
        tokens = ['Hello', 'world']
        generator.calculate_probabilities(tokens)
        probabilities_table = generator.get_probabilities_table()
        self.assertEqual(probabilities_table,
                         {'': [('Hello', 0.5), ('world', 0.5)],
                          'Hello': [('world', 1.0)]})

    def test_two_same_tokens(self):
        generator = MarkovChainGenerator(1)
        tokens = ['Hello', 'Hello']
        generator.calculate_probabilities(tokens)
        probabilities_table = generator.get_probabilities_table()
        self.assertEqual(probabilities_table,
                         {'': [('Hello', 1.0)],
                          'Hello': [('Hello', 1.0)]})

    def test_sentence(self):
        generator = MarkovChainGenerator(1)
        tokens = ['sentence', 'is', 'sentence', 'too']
        generator.calculate_probabilities(tokens)
        probabilities_table = generator.get_probabilities_table()
        self.assertEqual(probabilities_table,
                         {'': [('is', 0.25), ('sentence', 0.5), ('too', 0.25)],
                          'is': [('sentence', 1.0)],
                          'sentence': [('is', 0.5), ('too', 0.5)]})

    def test_depth2(self):
        generator = MarkovChainGenerator(2)
        tokens = ['Alpha', 'beta', 'gamma', '123']
        generator.calculate_probabilities(tokens)
        probabilities_table = generator.get_probabilities_table()
        self.assertEqual(probabilities_table,
                         {'': [('123', 0.25), ('Alpha', 0.25), ('beta', 0.25), ('gamma', 0.25)],
                          'Alpha': [('beta', 1.0)],
                          'beta': [('gamma', 1.0)],
                          'gamma': [('123', 1.0)],
                          'Alpha beta': [('gamma', 1.0)],
                          'beta gamma': [('123', 1.0)]})

def test(*args):
    unittest.main()


def set_parser():

    def configure_tokenize_parser(subparsers):
        parser_tokenize = subparsers.add_parser('tokenize')
        parser_tokenize.set_defaults(handler=print_tokens)

    def configure_probabilities_parser(subparsers):
        parser_probabilities = subparsers.add_parser('probabilities')
        parser_probabilities.add_argument('--depth', type=int, required=True, choices=range(1, 21))
        parser_probabilities.set_defaults(handler=probabilities)

    def configure_generate_parser(subparsers):
        parser_generate = subparsers.add_parser('generate')
        parser_generate.add_argument('--depth', type=int, required=True, choices=range(1, 21))
        parser_generate.add_argument('--size', type=int, required=True, choices=range(1, 10000))
        parser_generate.set_defaults(handler=generate)

    def configure_test_parser(subparsers):
        parser_test = subparsers.add_parser('test')
        parser_test.set_defaults(handler=test)

    parser = argparse.ArgumentParser(prog='Text generation with Markov chain')
    subparsers = parser.add_subparsers()

    configure_tokenize_parser(subparsers)
    configure_probabilities_parser(subparsers)
    configure_generate_parser(subparsers)
    configure_test_parser(subparsers)

    return parser


def main():
    parser = set_parser()

    with open('input.txt', encoding='utf-8') as input_stream:
        args = input_stream.readline()
        args = parser.parse_args(args.split())
        args.handler(input_stream, args)


if __name__ == '__main__':
    main()
