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
        search = SearchManga("The Beginning after", threaded=True)
        results = list(search.results())
        print(results)
        for i in results:
            print(str(i))
        first = results[0].url
        print("'",first,"'",)
        info = MangaInfo(first)
        print("'",info.results().title,"'",)
        print("'",info.results().chapters,"'",)
        #print("'",info.results().description,"'",)
        print("'",info.results().icon,"'",)
        #print("'",info.results().genres,"'",)
        #print("'",info.results().authors,"'",)
        #print("'",info.results().status,"'",)
        chapter = info.results().chapters[0]
        print("CHAPTER :: ", chapter)
        # time.sleep(1)
        print("CHAPTER URL :: ", chapter.url)
        chapterIn = ChapterInfo(chapter)
        imageLIST = chapterIn.results().image_urls
        print(imageLIST)
        file = f"D:/mangaPdf.pdf"

        # Download the chapter
        dl = DownloadChapter(chapter.url, file, imageLIST).results()

        print(f"Downloaded: {dl.saved_ok}")


    main()
