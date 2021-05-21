import string
import typing
import dataclasses
import lxml

from bs4 import BeautifulSoup

from manganelo.api.apibase import APIBase


@dataclasses.dataclass(frozen=True)
class MangaSearchResult:
	title: str
	url: str


class SearchManga(APIBase):
	def __init__(self, query: str, *, threaded: bool = False) -> None:
		"""
		Constructor for the object. We send the request here.

		:param str query: Query string which we will use as part of the URL which we will generate.
		:param bool threaded: Determines if we want to send the request on the main thread or spawn a new thread.
		"""

		self.url = None
		self.url2 = None
		self.url3 = None

		self._query = query
		self._response = None
		self._response2 = None
		self._response3 = None

		super(SearchManga, self).__init__(threaded)

	def _start(self) -> None:
		"""
		We generate the URL here and send the request.

		:raise: Exceptions from the requests module can be raised
		"""

		# Generate the URL, which includes removing 'illegal' characters
		self.url = self._generate_url(self._query)
		# print(self.url)

		self._response = self.send_request(self.url)
		# print(self._response)
		self.url2 = self.url.replace("page=1", "page=2")
		self.url3 = self.url.replace("page=1", "page=3")
		self._response2 = self.send_request(self.url2)
		self._response3 = self.send_request(self.url3)
		# print(self.url2)
		# print(self.url3)

	def results(self) -> typing.Generator[MangaSearchResult, None, None]:
		"""
		Extract the results from the request we sent earlier.
		[Threaded] We join the thread, which means that we wait for the request to finish.

		:return Generator: Return a generator of the results
		"""

		self._join_thread()

		# Entire page soup
		soup = BeautifulSoup(self._response.text, "lxml")
		soup2 = BeautifulSoup(self._response2.text, "lxml")
		soup3 = BeautifulSoup(self._response3.text, "lxml")
		# print(soup)
		# List of the search results
		results = soup.find_all(class_="manga-list-4-item-title")
		results2 = soup2.find_all(class_="manga-list-4-item-title")
		results3 = soup3.find_all(class_="manga-list-4-item-title")
		# print(results)

		# Iterate over the results soup and extract the information we want
		for i, ele in enumerate(results):
			manga = ele.a

			title = manga.get("title", None)  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'
			full_link = "https://fanfox.net"+link
			# print(title,full_link)
			yield MangaSearchResult(title=title, url=full_link)

		for i, ele in enumerate(results2):
			manga = ele.a

			title = manga.get("title", None)  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'
			full_link = "https://fanfox.net"+link
			# print(title,full_link)
			yield MangaSearchResult(title=title, url=full_link)
		for i, ele in enumerate(results3):
			manga = ele.a

			title = manga.get("title", None)  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'
			full_link = "https://fanfox.net"+link
			# print(title,full_link)
			yield MangaSearchResult(title=title, url=full_link)

	@staticmethod
	def _generate_url(query: str) -> str:
		"""
		Generate the URL we send the request to, we remove all 'illegal' characters here from the query string.

		:param str query: The base query string which we are searching for
		:return str: Return the formatted URL
		"""
		allowed_characters: str = string.ascii_letters + string.digits + "+"

		query = "".join([char.lower() for char in query.replace(" ", "+") if char in allowed_characters])

		return "https://fanfox.net/search?page=1&title=" + query
