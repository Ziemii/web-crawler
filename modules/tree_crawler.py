from urllib.parse import urlparse
from .proto_crawler import ProtoCrawler
from .site_node import SiteNode
from .results_printer import ResultsPrinter


class TreeCrawler(ProtoCrawler, ResultsPrinter):
    """
    Starts at provided address and continues asynchronously
    through related pages saving relations using nodes
    """
    def __init__(self, address: str):
        super().__init__(address)
        self._tree: SiteNode = SiteNode(self._root_address)

    async def _crawl_page(self, address):
        if address in self._visited_pages:
            return
        else:
            page_as_text: str or False = await self._try_to_get_page_as_text(address)
            if not page_as_text:
                return

        links_on_page: set = self._find_all_links(page_as_text)
        relatives: set = self._find_relative_addresses(links_on_page)

        subpages: list[str] = urlparse(address).path.split("/")
        cleaned_subpages: list[str] = [subpage for subpage in subpages if subpage != ""]

        await self._create_node_by_value(cleaned_subpages)
        await self._make_concurrent_requests(relatives, self._crawl_page)

    def _find_relative_addresses(self, addresses) -> set:
        relatives = set()
        for address in addresses:
            parsed_url = urlparse(address, allow_fragments=False)
            if self._is_address_valid_relative(parsed_url):
                relatives.add(
                    self._parsed_root_address.scheme
                    + "://"
                    + self._parsed_root_address.netloc
                    + parsed_url.path
                )
        return relatives

    async def _create_node_by_value(self, node_values) -> None:
        async with self._lock:
            current_node: SiteNode = self._tree
            subpages_count: int = len(node_values)
            counter: int = 0
            child_found: bool = False
            while counter < subpages_count:
                for child in current_node.children:
                    if node_values[counter] == child.value:
                        current_node = child
                        child_found = True
                        break
                if child_found:
                    child_found = False
                    counter += 1
                else:
                    new_node = SiteNode(node_values[counter])
                    current_node.add_child(new_node)
                    current_node = new_node
                    counter += 1

    async def start_crawl(self) -> None:
        await self._crawl_page(self._tree.value)

    def print_results(self) -> None:
        print(self._tree)
