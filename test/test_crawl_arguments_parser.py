import unittest
from modules.crawl_arguments_parser import CrawlerParser


class TestArgumentsParser(unittest.TestCase):
    def test_arguments_parser_program_argument(self):
        testargs = ["crawl"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.program, testargs[0])

        testargs = ["print-tree"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.program, testargs[0])

    def test_arguments_parser_page_argument(self):
        testargs = ["crawl", "--page", "https://crawler-test.com////////"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.page, "https://crawler-test.com")

    def test_arguments_parser_format_argument(self):
        testargs = ["crawl", "--format", "json"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.format, testargs[2])

        testargs = ["crawl"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.format, "csv")

    def test_arguments_parser_output_argument(self):
        testargs = ["crawl", "--output", "C:/crawler_test"]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.output, testargs[2])

    def test_arguments_parser_multiple_arguments(self):
        testargs = [
            "crawl",
            "--page", "https://crawler-test.com",
            "--format", "json",
            "--output", "C:/crawler_test",
        ]
        parser = CrawlerParser(testargs)
        self.assertEqual(parser.program, testargs[0])
        self.assertEqual(parser.page, testargs[2])
        self.assertEqual(parser.format, testargs[4])
        self.assertEqual(parser.output, testargs[6])
