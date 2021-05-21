
import manganelo
import MangaHub
import kissmanga
import fanfox

# manganelo==1.5.1

try:
    searchStr = input("manga : > ")               # title Input
    search = manganelo.SearchManga(searchStr, threaded=False)
    results = list(search.results())
    count = 1
    if len(results) == 0:
        print(" No results found with the name ..")
        exit(0)
    for i in results:
        print(count, "\t\t", i.title)   # result 1
        count += 1

    in1 = int(input())                 # Manga choose Input
    first_result = results[in1-1].url
    MangaName = results[in1-1].title
    info = results[in1-1]

    try:
        info2 = kissmanga.SearchManga(MangaName, threaded=True)
        results = list(info2.results())
        info2 = [i for i in results if MangaName.lower() == i.title.lower()]
        info2 = info2[0]
    except IndexError:
        info2 = None
    try:
        info3 = fanfox.SearchManga(MangaName, threaded=True)
        results = list(info3.results())
        info3 = [i for i in results if MangaName.lower() == i.title.lower()]
        info3 = info3[0]
    except IndexError:
        info3 = None
    try:
        info4 = MangaHub.SearchManga(MangaName, threaded=True)
        results = list(info4.results())
        info4 = [i for i in results if MangaName.lower() == i.title.lower()]
        info4 = info4[0]
    except IndexError:
        info4 = None

    print("info :: ", info)
    print("info2 :: ", info2)
    print("info3 :: ", info3)
    print("info4 :: ", info4)     # result 2
    # DataStructure = dir(info)
    # print(DataStructure)

    if info is None:
        print("manganelo not working..")
    if info2 is None:
        print("kissanime not working..")
    if info3 is None:
        print("fanfox not working..")
    if info4 is None:
        print("mangahub not working..")
    serverChoice = input("1.manganelo  2.kissanime  3.fanfox  4.mangahub\nChoose server : ")

    if serverChoice is '1':
        info = manganelo.MangaInfo(first_result)
        server = info
    elif serverChoice is '2':
        info2 = kissmanga.MangaInfo(info2.url)
        server = info2
    elif serverChoice is '3':
        info3 = fanfox.MangaInfo(info3.url)
        server = info3
    elif serverChoice is '4':
        info4 = MangaHub.MangaInfo(info4.url)
        server = info4

    chapter_list = server.results().chapters
    for l in chapter_list:
        print(l.num, "\t\t", l.title.strip("\n"))

    chapter_sChose = input()
    if "-" not in chapter_sChose:
        chap = int(chapter_sChose)
        k = server.results().chapters[chap-1]
        print(k)
    elif "-" in chapter_sChose:
        getRange = chapter_sChose.replace(" ", "")
        getRange = getRange.split("-")
        if len(getRange) == 2 and getRange[0].isdecimal() and getRange[1].isdecimal():
            lower = min(getRange)
            higher = max(getRange)
        for i in range(int(lower), int(higher)+1):
            print(server.results().chapters[i-1])
            print("::::::")
except Exception:
    exit(0)


# manga_info = MangaInfo("https://manganelo.com/manga/et923360", threaded=True)

# manga_page = manga_info.results()

# print("\n\n\n", manga_page)
# print(manga_page.chapters[-1].num)
