import dataclasses

from typing import List

from bs4 import BeautifulSoup

from .apibase import APIBase

import requests


@dataclasses.dataclass
class ChapterInformation:
	title: str
	url: str
	image_urls: List[str]


class ChapterInfo(APIBase):
	def __init__(self, src_url: str, *, threaded: bool = False):

		self._src_url = src_url

		self._soup = None

		self._start()

		super(ChapterInfo, self).__init__(threaded=threaded)

	@classmethod
	def from_soup(cls, soup: BeautifulSoup):
		return ChapterInformation(
			title=cls._get_chapter_title(soup),
			url="N/A",
			image_urls=cls._get_image_urls(soup)
		)

	def results(self):
		self._join_thread()

		return ChapterInformation(
			title=self._get_chapter_title(self._soup),
			url=self._src_url,
			image_urls=self._get_image_urls(self._soup)
		)

	def _start(self) -> None:
		mangaChapObj = self._src_url
		chapterUrl = mangaChapObj.url
		#print("::::", chapterUrl)
		#chrome_options = Options()
		#chrome_options.add_argument("--headless")
		# print("THIS IS EXECUTING")
		#browser = webdriver.Chrome(executable_path="C:\Program Files\chromedriver\chromedriver.exe", options=chrome_options)
		# browser = webdriver.Firefox()
		#browser.get(chapterUrl)
		# wait for the element to load
		#try:
		#	WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-manga-chapter-img")))
		#except TimeoutException:
		#	print("TimeoutException: Element not found")
		#	return None
		# print(element)
		#response = browser.page_source
		response = self.send_request(chapterUrl)
		self._soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")

	@classmethod
	def _get_image_urls(cls, uniformRes) -> List[str]:
		"""
		Return all the image URLS inside the soup object.

		:return: We return a list of image URLS
		"""
		'''
		#chrome_options = Options()
		#chrome_options.add_argument("--headless")
		#print("THIS IS EXECUTING")
		#browser = webdriver.Chrome(executable_path="C:\Program Files\chromedriver\chromedriver.exe", options=chrome_options)
		#browser = webdriver.Firefox()
		#browser.get(uniformRes)
		#wait for the element to load
		#try:
		#	element = WebDriverWait(browser, 3).until(
		#		EC.presence_of_element_located((By.CLASS_NAME, "reader-main-img")))
		#except TimeoutException:
		#	print("TimeoutException: Element not found")
		#	return None

		#print(element)
		#soup = browser.page_source
		#soup = BeautifulSoup(soup, "lxml")'''

		def valid(url: str):
			return ".jpg" in url or ".png" in url or ".gif" in url
		divSoup = uniformRes.find("div", {"id": "mangareader"})
		print("div soup :::", divSoup)
		image_soup = divSoup.find_all("img")
		images = [url[url.index("https://"):] for url in map(lambda ele: ele["src"], image_soup) if valid(url)]
		one = images[0]
		images.clear()
		images.append(one)
		oneImg = images[0]
		ext = oneImg[-4:]
		print(ext)
		res = oneImg.rindex("/")
		print(res)
		curr = oneImg[res+1:]
		curr = int(curr.replace(ext,""))
		count = 1
		for i in range(1,350):
			imgs = oneImg[:res + 1] + str(curr + count) + ext
			images.append(imgs)
			count += 1
		# print(images)
		return images

	@classmethod
	def _get_chapter_title(cls, soup: BeautifulSoup) -> str:
		""" Return the title of the chapter. """
		# print("soup::\n",soup)
		try:
			title = soup.find("h3").text
			print("Chapter Title :: ", title)
		except AttributeError:
			title = "Manga"
		return title if title else "None"
