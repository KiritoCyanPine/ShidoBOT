import os
import shutil
import tempfile
import typing
import dataclasses

from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from PIL import Image

from .apibase import APIBase
from .chapterinfo import ChapterInfo


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@dataclasses.dataclass
class ChapterStatus:
	title: str
	saved_ok: bool
	percent_saved: float
	path: str


class DownloadChapter(APIBase):

	def __init__(self, src_url: str, dst_path: str, URLSofImg: list, *, threaded: bool = False):
		"""
		Object constructor

		:param src_url: The  chapter which we will be downloading
		:param dst_path: The path where the chapter will be saved after completion
		:param threaded: Whether the bulk of the work will be done on a different thread or the main thread
		"""

		self._src_url = src_url
		self._dst_path = dst_path
		self._title = None

		self._saved = False
		self._percent_saved = 0
		self._image_urls = URLSofImg

		super(DownloadChapter, self).__init__(threaded)

	def results(self):
		"""
		Returns the status of the download.

		:return ChapterStatus: The status of the chapter
		"""

		self._join_thread()

		return ChapterStatus(
			saved_ok=self._saved,
			percent_saved=self._percent_saved,
			path=self._dst_path,
			title=self._title
		)

	def _start(self):
		""" The main function...Where the magic happens. """
		print("self._src_url  : ", self._src_url)
		r = self.send_request(self._src_url)

		soup = BeautifulSoup(r.text, "lxml")
		chap = ChapterInfo.from_soup(soup)

		self._title = chap.title
		print("Chap title : ", self._title)

		with tempfile.TemporaryDirectory() as temp_dir:
			image_paths = self._download_images(self._image_urls, temp_dir)

			num_pages = self._create_pdf(image_paths)

			self._percent_saved = num_pages / len(chap.image_urls)

	def _download_images(self, image_urls: typing.List[str], save_dir: str) -> typing.List[str]:
		"""
		Download images from a sequence of URLS into a directory.

		:param image_urls: List of URLS which we will attempt to download here
		:param save_dir: The directory where the downloaded images will be saved
		:return list: List of paths where the downloaded images are stored
		"""

		image_paths = []

		for i, url in enumerate(image_urls):
			chrome_options = Options()
			chrome_options.add_argument("start-maximized")
			chrome_options.add_argument("--headless")
			chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
			chrome_options.add_experimental_option('useAutomationExtension', False)
			print("THIS IS EXECUTING")
			browser = webdriver.Chrome(executable_path="C:\Program Files\chromedriver\chromedriver.exe", options=chrome_options)
			# browser = webdriver.Firefox()
			print(url)
			browser.get(url)
			image = browser.page_source
			print("CONTENT: ",image)
			# image = self.send_request("http:"+url)

			image_ext = url.split(".")[-1]
			imageName = f"{i}.{image_ext}"
			a = imageName.index(".jpg")
			imageName = imageName[:a + 4]

			image_dst_path = os.path.join(save_dir, imageName)

			if image is not None:
				with open(image_dst_path, "wb") as fh:

					# Magic boolean which makes it work
					print(image)
					image.raw.decode_content = True

					# noinspection PyBroadException

					# Attempt to download the image from the URL
					try:
						shutil.copyfileobj(image.raw, fh)

					# We should reduce the scope
					except Exception:
						pass

					# We downloaded the image without any errors
					else:
						image_paths.append(image_dst_path)

		return image_paths

	def _create_pdf(self, images: typing.List[str]) -> int:
		"""

		:param images: List of image paths which we will attempt to convert into a PDF
		:return int: The number of pages in the PDF
		"""

		pdf = canvas.Canvas(self._dst_path)

		num_pages = 0

		for image in images:
			try:
				with Image.open(image) as img:
					w, h = img.size

			except (OSError, UnboundLocalError):
				continue

			# Set the page dimensions to the image dimensions
			pdf.setPageSize((w, h))

			try:
				# Insert the image onto the current page
				pdf.drawImage(image, x=0, y=0)

			except OSError:
				continue

			# Create a new page ready for the next image
			pdf.showPage()

			num_pages += 1

		if num_pages > 0:
			dirs = os.path.dirname(self._dst_path)

			# Create the path if it doesn't exist already
			if dirs:
				os.makedirs(dirs, exist_ok=True)

			try:
				pdf.save()
			except FileNotFoundError:
				pass

			else:
				self._saved = True

		return num_pages
