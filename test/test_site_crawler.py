import unittest


class TestSiteCrawler(unittest.TestCase):
    async def test_start_crawl(self):
        site_crawler = SiteCrawler("")
        site_crawler._crawl_page = MagicMock()
        site_crawler.start_crawl()
        site_crawler._crawl_page.assert_called_once()
