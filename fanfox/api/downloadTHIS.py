import os
import shutil
import tempfile
import typing
import dataclasses

from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from PIL import Image

from api.apibase import APIBase
from api.chapterinfo import ChapterInfo


@dataclasses.dataclass
class ChapterStatus:
    title: str
    saved_ok: bool
    percent_saved: float
    path: str

class DownloadChapter(APIBase):
	_src_url: str