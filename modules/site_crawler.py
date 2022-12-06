import sys
import os
import re
from urllib.parse import urlparse
from pathlib import Path
import json
import csv
from .proto_crawler import ProtoCrawler
from .save_on_disk import SaveResultsToCSV, SaveResultsToJSON


class SiteCrawler(ProtoCrawler, SaveResultsToCSV, SaveResultsToJSON):
    """
    Starts at provided address and continues asynchronously
    through related pages collecting data in process.
    """

    def __init__(self, address: str):
        super().__init__(address)
        self._pages = {}

    async def _crawl_page(self, address):
        if address in self._visited_pages:
            try:
                async with self._lock:
                    self._pages[address]["reference count"] += 1
            except KeyError:
                return
            return
        else:
            page_as_text: str or False = await self._try_to_get_page_as_text(address)
            if not page_as_text:
                return

        page_title: str = self._try_to_get_page_title(page_as_text)
        links_on_page: set = self._find_all_links(page_as_text)

        externals, relatives = self._find_external_and_relative_addresses(links_on_page)

        async with self._lock:
            self._pages[address] = {
                "url": address,
                "page title": page_title,
                "internal links count": len(relatives),
                "external links count": len(externals),
                "reference count": 1 if address != self._root_address else 0,
            }

        await self._add_reference_to_root_if_in_externals(externals)
        await self._make_concurrent_requests(relatives, self._crawl_page)

    def _try_to_get_page_title(self, page_as_text) -> str:
        try:
            return re.search(
                r"(?<=<title>)([\'\"\d\w\s\-\=\,.?]*)(?=</title>)", page_as_text
            ).group(1)
        except AttributeError:
            return ""

    def _find_external_and_relative_addresses(self, addresses) -> tuple:
        externals = set()
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
            elif parsed_url.scheme == "http" or parsed_url.scheme == "https":
                externals.add(address)
        return (externals, relatives)

    async def _add_reference_to_root_if_in_externals(self, addresses) -> None:
        for address in addresses:
            parsed_url = urlparse(address)
            if parsed_url.netloc == self._parsed_root_address.netloc:
                try:
                    async with self._lock:
                        self._pages[self._root_address]["reference count"] += 1
                except KeyError:
                    print("\nERROR: Root page key not present. Shutting down.")
                    sys.exit(1)

    def save_results_to_json(self, directory) -> None:
        self._check_output_location(directory)
        try:
            with open(
                Path(directory).as_posix() + "/results.json", "w", encoding="utf-8"
            ) as outfile:
                json.dump(self._pages, outfile, indent=2)
        except (FileNotFoundError, PermissionError) as error:
            print(f"Could not save output file. Reason: {error}. Please try again.")

    def save_results_to_csv(self, directory) -> None:
        self._check_output_location(directory)
        page_info = [
            "url",
            "page title",
            "internal links count",
            "external links count",
            "reference count",
        ]
        try:
            with open(
                Path(directory).as_posix() + "/results.csv",
                "w",
                encoding="utf-8",
                newline="",
            ) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=page_info)
                writer.writeheader()
                for value in self._pages.values():
                    writer.writerow(value)
        except (FileNotFoundError, PermissionError) as error:
            print(f"Could not save output file. Reason: {error}. Please try again.")

    def _check_output_location(self, directory) -> None:
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as error:
            print(f"Can't access given directory. Reason: {error}. Please try again.")

    async def start_crawl(self) -> None:
        await self._crawl_page(self._root_address)
