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


@dataclasses.dataclass(frozen=True)
class MangaChapter:
    url: str
    title: str
    num: float


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

        Title = str(self._soup.find(class_="post-title").find("h1").text).replace("\n", "")

        return Title

    def _get_icon(self) -> str:
        imageUrl = self._soup.find(class_="summary_image").find("img").attrs.get("src")

        return imageUrl

    def _get_description(self) -> str:
        description = self._soup.find(class_="summary__content").find("p").text

        return description

    def _get_chapter_list(self) -> typing.List[MangaChapter]:
        """
        Extract the chapter list from the website

        :return list: Return a list of chapters which each contain information about the chapter
        """
        ls = []
        count = 1
        try:
            panels = self._soup.find(class_="version-chap")
            for i, ele in enumerate(reversed(panels.find_all("li"))):
                if ele is not None:
                    url = ele.find("a")["href"]
                    text = ele.find("a").text
                    c = MangaChapter(url=url, num=count, title=text)
                    count += 1
                    ls.append(c)
        except Exception:
            pass
        # ls = sorted(ls, key=lambda x: [k for k in x.title], reverse=False)
        # print(ls)
        return ls

    # noinspection PyDictCreation
    def _parse_table(self) -> dict:
        """
        Parse the main table which contains the key information

        return dict: A dict of values taken from the page
        """

        data = {}
        try:
            data["author"] = str(self._soup.find(class_="author-content").text).replace("\n", "")
        except AttributeError:
            data["author"] = "N/A"
        try:
            data["genres"] = [ele.text for ele in self._soup.find(class_="genres-content").find_all("a")]
        except AttributeError:
            data["genres"] = ["N/A"]
        try:
            data["icon"] = self._soup.find(class_="summary_image").find("img").attrs.get("src")
        except AttributeError:
            data["icon"] = None
        try:
            data["description"] = self._soup.find(class_="description-summary").find("p").text
        except AttributeError:
            data["description"] = "N/A"
        try:
            data["status"] = str(self._soup.find(class_="post-status").find_all(class_="post-content_item"))

            if "OnGoing" in data["status"]:
                data["status"] = "OnGoing"
            elif "Completed" in data["status"]:
                data["status"] = "Completed"
            else:
                data["status"] = "On-Hold"
        except AttributeError:
            data["status"] = "N/A"

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
