from halo import Halo
from .crawl_arguments_parser import CrawlerParser
from .site_crawler import SiteCrawler
from .tree_crawler import TreeCrawler


class Crawlers:
    """Entry point for crawlers program"""
    def __init__(self, arguments):
        self._arguments: str = CrawlerParser(arguments)
        self._site_crawler: str = SiteCrawler(self._arguments.page)
        self.tree_crawler: str = TreeCrawler(self._arguments.page)

    async def perform_crawl(self) -> None:
        """Makes call to appropriate class methods based on arguments"""
        if self._arguments.program == "crawl":
            await self._site_crawl()

            if self._arguments.format == "json":
                self._site_crawler.save_results_to_json(self._arguments.output)
            elif self._arguments.format == "csv":
                self._site_crawler.save_results_to_csv(self._arguments.output)
            print("Done.")

        if self._arguments.program == "print-tree":
            await self._tree_crawl()
            print("Done.")

    async def _site_crawl(self) -> None:
        with Halo(text=f"Crawling {self._arguments.page}", spinner="dots"):
            await self._site_crawler.start_crawl()
        print("Crawling done.")

    async def _tree_crawl(self) -> None:
        with Halo(text=f"Building tree for {self._arguments.page}", spinner="dots"):
            await self.tree_crawler.start_crawl()
        self.tree_crawler.print_results()
