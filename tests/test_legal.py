import unittest

from webservices.resources.legal import parse_query_string

class LegalPhraseSearchTests(unittest.TestCase):
    def test_parse_query_no_phrase(self):
        parsed = parse_query_string('hello world')
        self.assertEquals(parsed, dict(terms=['hello world'], phrases=[]))

    def test_parse_query_with_phrase(self):
        parsed = parse_query_string('require "electronic filing" 2016')
        self.assertEquals(parsed, dict(terms=['require', '2016'], phrases=['electronic filing']))

    def test_parse_query_with_many_phrases(self):
        parsed = parse_query_string('require "electronic filing" 2016 "sans computer"')
        self.assertEquals(parsed, dict(terms=['require', '2016'], phrases=['electronic filing', 'sans computer']))
