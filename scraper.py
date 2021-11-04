import html
import requests
from lxml import html as xhtml


def extract_songs_data(x_tree):

    for op_ed in ["opnening", "ending"]:
        main_template = f'//div[@class="theme-songs js-theme-songs {op_ed}"]'

        songs = list(filter(lambda elem: elem != "",
                            map(lambda elem: html.unescape(elem).strip().strip("\""),
                                x_tree.xpath(f'{main_template}//span[@class="theme-song-title"]/text()')
                                )
                            ))
        if not songs:
            songs = list(filter(lambda elem: elem != "",
                                map(lambda elem: html.unescape(elem).strip().strip("\""),
                                    x_tree.xpath(f'{main_template}//td[2]/text()')
                                    )
                                ))

        artists = list(map(lambda elem: html.unescape(elem).strip(),
                           x_tree.xpath(f'{main_template}//span[@class="theme-song-artist"]/text()')
                           ))

        episodes = list(map(lambda elem: html.unescape(elem).strip(),
                            x_tree.xpath(f'{main_template}//span[@class="theme-song-episode"]/text()')
                            ))

        if not episodes:
            episodes = ["all" for _ in range(len(songs))]

        yield list(zip([("OP" if op_ed == "opnening" else "ED") for _ in range(len(songs))],
                       songs,
                       artists,
                       episodes))


def scrape(anime_codes):
    for anime_code in anime_codes:
        page = requests.get(f"https://myanimelist.net/anime/{anime_code}")
        if page.status_code == 200:
            tree = xhtml.fromstring(page.content.decode('utf-8'))
            name = html.unescape(tree.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()')[0]).strip()
            print(f'{anime_code}-{name}')
            for elem in extract_songs_data(tree):
                print(f'\t{elem})')
