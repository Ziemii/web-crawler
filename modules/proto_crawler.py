import re
import asyncio
from urllib.parse import urlparse, ParseResult
from abc import ABC, abstractmethod
from http import HTTPStatus
from aiohttp.client_reqrep import ClientResponse
from aiohttp_requests import requests
import aiohttp.client_exceptions as aiohttpErrors


class ProtoCrawler(ABC):
    """Abstracted-out shape and methods common across concrete crawlers"""

    def __init__(self, address: str):
        self._parsed_root_address: ParseResult = urlparse(address)
        self._root_address: str = (
            self._parsed_root_address.scheme
            + "://"
            + self._parsed_root_address.netloc
            + self._parsed_root_address.path
            + "/"
        )
        self._lock: asyncio.Lock = asyncio.Lock()
        self._visited_pages: set = set()

    async def _try_to_get_page_as_text(self, address) -> str or False:
        async with self._lock:
            self._visited_pages.add(address)
        try:
            response: ClientResponse = await requests.get(
                address, allow_redirects=False
            )
            return await response.text()
        except (aiohttpErrors.ClientError, UnicodeDecodeError, UnicodeError):
            return False
        if response.status >= HTTPStatus.BAD_REQUEST:
            return False

    async def _make_concurrent_requests(self, addresses, function) -> None:
        asyncio_tasks = set()
        for address in addresses:
            task = asyncio.create_task(function(address))
            asyncio_tasks.add(task)
            task.add_done_callback(asyncio_tasks.discard)
        await asyncio.gather(*asyncio_tasks)

    def _find_all_links(self, page_as_text) -> set:
        return set(re.findall(r"<a.*href=\"(\S+)\"", page_as_text))

    def _is_address_valid_relative(self, parsed_address) -> bool:
        return all(
            [
                parsed_address.netloc == "",
                parsed_address.path != "",
                parsed_address.path != "#",
                not re.search(r"([x]{10})", parsed_address.path),
            ]
        )

    @abstractmethod
    async def start_crawl(self):
        """Method for starting crawl process"""
