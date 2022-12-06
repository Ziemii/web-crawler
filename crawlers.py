import sys
import asyncio
from modules.crawlers import Crawlers


async def main():
    crawlers = Crawlers(sys.argv[1:])
    await crawlers.perform_crawl()


if __name__ == "__main__":
    asyncio.run(main())
