import unittest


class TestTreeCrawler(unittest.TestCase):
    async def test_start_crawl(self):
        tree_crawler = TreeCrawler("")
        tree_crawler._crawl_page = unittest.MagicMock()
        tree_crawler.start_crawl()
        tree_crawler._crawl_page.assert_called_once()
