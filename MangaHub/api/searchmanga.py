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

		self._query = query
		self._response = None

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

	def results(self) -> typing.Generator[MangaSearchResult, None, None]:
		"""
		Extract the results from the request we sent earlier.
		[Threaded] We join the thread, which means that we wait for the request to finish.

		:return Generator: Return a generator of the results
		"""

		self._join_thread()

		# Entire page soup
		soup = BeautifulSoup(self._response.text, "lxml")
		# print(soup)
		# List of the search results
		results = soup.find_all(class_="media-heading")
		# print(results)

		# Iterate over the results soup and extract the information we want
		for i, ele in enumerate(results):
			manga = ele.a

			title = manga.text  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'

			# print(title,full_link)
			yield MangaSearchResult(title=title, url=link)

	@staticmethod
	def _generate_url(query: str) -> str:
		"""
		Generate the URL we send the request to, we remove all 'illegal' characters here from the query string.

		:param str query: The base query string which we are searching for
		:return str: Return the formatted URL
		"""
		allowed_characters: str = string.ascii_letters + string.digits + "+" + "%"

		query = "".join([char.lower() for char in query.replace(" ", f"%20") if char in allowed_characters])

		return "https://mangahub.io/search?q=" + query + "&post_type=wp-manga&op=&author=&artist=&release=&adult="
