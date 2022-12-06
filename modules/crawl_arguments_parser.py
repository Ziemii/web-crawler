from argparse import ArgumentParser, Namespace
from pathlib import Path


class CrawlerParser:
    """Parses arguments and exposes usable values."""

    def __init__(self, args):
        self._create_parser()
        self._add_arguments_to_parser()
        self._save_provided_arguments(args)

    def _create_parser(self):
        self._parser = ArgumentParser(
            usage="""
            crawler.py {program} [--page PAGE] [--format {csv or json}] [--output OUTPUT]
            
            For program you can choose:

                -"crawler" -crawls address and saves results in --output location
                -"print-tree" -prints page structure
            
            Both needs valid --page address to yield any meaningful results.

            Crawler ptional arguments:

                --format -you can choose between csv or json(default is csv)
                --output -location for crawler results(default is current script location)

            Example uses:

                crawler.py crawl  --page https://test-crawler.com --format json --output C:/crawler_results
        
                crawler.py print-tree --page https://test-crawler.com


            """
        )

    def _add_arguments_to_parser(self):
        self._parser.add_argument("program", choices=["crawl", "print-tree"])
        self._parser.add_argument(
            "--page", help="Address of page to crawl", default="https://example.com"
        )
        self._parser.add_argument(
            "--format",
            help="Choose csv or json output format",
            default="csv",
            choices=["csv", "json"],
        )
        self._parser.add_argument(
            "--output",
            help="Path of output location",
            default=Path(__file__).parent.parent,
        )

    def _save_provided_arguments(self, args) -> None:
        arguments: Namespace = self._parser.parse_args(args)
        self._program: str = arguments.program
        self._page: str = arguments.page.rstrip('/')
        self._format: str = arguments.format
        self._output: str = arguments.output

    @property
    def program(self) -> str:
        """Returns name of program to run"""
        return self._program

    @property
    def page(self) -> str:
        """Returns target crawl address"""
        return self._page

    @property
    def format(self) -> str:
        """Returns chosen output format"""
        return self._format

    @property
    def output(self) -> str:
        """Returns file output location"""
        return self._output
