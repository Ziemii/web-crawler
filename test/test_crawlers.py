import unittest


class TestCrawlers(unittest.TestCase):
    async def test_perform_crawl(self):
        crawlers = Crawlers(["crawl"])
        crawlers._site_crawl = MagicMock()
        crawlers.perform_crawl()
        crawlers._site_crawl.assert_called_once()

        crawlers = Crawlers(["print-tree"])
        crawlers._tree_crawl = MagicMock()
        crawlers.perform_crawl()
        crawlers._tree_crawl.assert_called_once()
