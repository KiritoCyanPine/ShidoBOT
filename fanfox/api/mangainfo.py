import dataclasses
import typing

from bs4 import BeautifulSoup

from .apibase import APIBase


@dataclasses.dataclass(frozen=True)
class MangaData:
    url: str
    title: str
    authors: list
    status: str
    genres: list
    chapters: list
    icon: str
    description: str


@dataclasses.dataclass(frozen=False)
class MangaChapter:
    url: str
    title: str
    num: float

    def changeNumVal(self, value):
        self.num = value


# noinspection PyBroadException
class MangaInfo(APIBase):
    def __init__(self, src_url: str, *, threaded: bool = False):
        """
        Constructor for the object. We send the request here.

        :param str src_url: The URL which we will send a request to
        :param bool threaded: Determines if we want to send the request on the main thread or spawn a new thread.
        """

        self._src_url = src_url

        self._soup = None

        super(MangaInfo, self).__init__(threaded)

    def _start(self) -> None:
        """ Send the request and create the soup object """

        response = self.send_request(self._src_url)

        self._soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")

    def results(self) -> MangaData:
        """ Performs the soup extraction and returns an object """

        self._join_thread()

        table = self._parse_table()

        r = MangaData(
            url=self._src_url,
            title=self._get_title(),
            status=table.get("status", None),
            authors=table.get("author", []),
            genres=table.get("genres", []),
            chapters=self._get_chapter_list(),
            icon=table.get("icon", None),
            description=table.get("description", None),

        )

        return r

    def _get_title(self) -> typing.Union[str, None]:
        """ Return the title present on the page """

        story_info_right = self._soup.find(class_="detail-info-right-title-font")

        return getattr(story_info_right, "text", None)

    def _get_icon(self) -> str:
        info_panel = self._soup.find(class_="panel-story-info")
        info_left = info_panel.find(class_="story-info-left")
        image = info_left.find(class_="info-image")

        return image.find("img").get("src", None)

    def _get_description(self) -> str:
        info_panel = self._soup.find(class_="panel-story-info")
        description = info_panel.find(class_="panel-story-info-description")

        return description.text.replace("Description :", "").strip()

    def _get_chapter_list(self) -> typing.List[MangaChapter]:
        """
        Extract the chapter list from the website

        :return list: Return a list of chapters which each contain information about the chapter
        """
        ls = []
        count = 1
        try:
            panels = self._soup.find("div", {"id": "list-1"})
            for i, ele in enumerate(reversed(panels.find_all("li"))):
                if ele is not None:
                    url = "https://fanfox.net/"+ele.find("a")["href"]
                    text = ele.find("a").text

                    c = MangaChapter(url=url, num=count, title=text)
                    ls.append(c)
        except Exception:
            pass
        try:
            panels = self._soup.find("div", {"id": "list-2"})

            for i, ele in enumerate(reversed(panels.find_all("li"))):
                if ele is not None:
                    url = "https://fanfox.net/" + ele.find("a")["href"]
                    text = ele.find("a").text

                    c = MangaChapter(url=url, num=count, title=text)
                    ls.append(c)
        except Exception:
            pass
        ls = sorted(ls, key=lambda x: [k for k in x.title.split() if "Ch." in k], reverse=False)
        for i in ls:
            i.num = count
            count += 1
        return ls

    # noinspection PyDictCreation
    def _parse_table(self) -> dict:
        """
        Parse the main table which contains the key information

        return dict: A dict of values taken from the page
        """

        data = {}
        data["author"] = self._soup.find(class_="detail-info-right-say").text
        data["genres"] = [ele.text for ele in self._soup.find(class_="detail-info-right-tag-list").find_all("a")]
        data["status"] = self._soup.find(class_="detail-info-right-title-tip").text
        data["icon"] = self._soup.find(class_="detail-info-cover-img").attrs.get("src")
        data["description"] = self._soup.find(class_="detail-info-right-content").text
        return data


'''
    def _parse_extended_table(self) -> object:
        """
        Extract information from the extended table

        :return dict: Dict containing information taken from the extended table
        """

        right_extend = self._soup.find(class_="story-info-right-extent")

        rows = [ele.text for ele in right_extend.find_all("span", class_="stre-value") if ele.text.strip()]

        updated, views, *_ = rows

        # Remove AM and PM
        updated = updated[0:-3]

        updated = datetime.strptime(updated, "%b %d,%Y - %H:%M")
        views = int(views.replace(",", ""))

        return {"updated": updated, "views": views}'''
