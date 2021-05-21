# noinspection PyUnresolvedReferences
from .api import (MangaInfo, SearchManga, DownloadChapter, ChapterInfo)
import time
__ALL__ = (
    "MangaInfo",
    "SearchManga",
    "DownloadChapter",
    "ChapterInfo"
)

if __name__ == "__main__":
    def main():
        search = SearchManga("Zero Game", threaded=False)
        results = list(search.results())
        for i in results:
            print(str(i))
        first = results[0].url
        print(first)
        info = MangaInfo(first)
        print(info.results().chapters)
        chapter = info.results().chapters[0]
        print(chapter)
        time.sleep(1)
        chapterIn = ChapterInfo(chapter)
        imageLIST = chapterIn.results().image_urls
        print(imageLIST)
        file = f"D:/mangaPdf.pdf"

        # Download the chapter
        dl = DownloadChapter(chapter.url, file, imageLIST).results()

        print(f"Downloaded: {dl.saved_ok}")

    main()
