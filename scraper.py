import html
import requests
from lxml import html as xhtml


def extract_songs_data(x_tree):
    for op_ed in ["opnening", "ending"]:
        main_template = f'//div[@class="theme-songs js-theme-songs {op_ed}"]'

        songs = list(filter(lambda elem: elem != "",
                            map(lambda elem: clean(elem),
                                x_tree.xpath(f'{main_template}//span[@class="theme-song-title"]/text()')
                                )
                            ))
        if not songs:
            songs = list(filter(lambda elem: elem != "",
                                map(lambda elem: clean(elem),
                                    x_tree.xpath(f'{main_template}//td[2]/text()')
                                    )
                                ))

        artists = list(map(lambda elem: clean(elem, 3),
                           x_tree.xpath(f'{main_template}//span[@class="theme-song-artist"]/text()')
                           ))

        episodes = list(map(lambda elem: clean(elem),
                            x_tree.xpath(f'{main_template}//span[@class="theme-song-episode"]/text()')
                            ))

        if not episodes:
            episodes = ["all" for _ in range(len(songs))]

        yield list(zip(songs,
                       artists,
                       episodes))


def clean(string, extra=0):
    return html.escape(html.unescape(string).strip().strip("\""))[extra:]


def scrape(anime_code):
    page = requests.get(
        f"https://www.myanimelist.net/anime/{anime_code}",
        headers={
            "Referer": "https://www.google.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }, )
    if page.status_code == 200:
        tree = xhtml.fromstring(page.content.decode('utf-8'))
        name = clean(tree.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()')[0])
        print(f'{anime_code}-{name}')
        for elem in extract_songs_data(tree):
            yield anime_code, name, elem
    else:
        print(anime_code, page.status_code)
        if page.status_code == 403:
            print("BLOCKED!!")
            exit(0)

# for elem in scrape(15):
#     print(elem)

# op = True
# for (anime_code, name, ops) in scrape(20583):
#     for (song_name, artist, eps) in ops:
#         print("OP" if op else "ED", song_name, artist, eps)
#     op = False
