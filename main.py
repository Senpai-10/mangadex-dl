import requests
import argparse
import time
from dataclasses import dataclass, field


def parse_filename(f) -> tuple[str, str]:
    num = ""
    parts = f.split("-")
    page_number = parts[0]
    file_ext = parts[1].split(".")[1]

    for char in page_number:
        if not char.isdigit():
            continue

        num += char

    return (num, f"{num}.{file_ext}")


@dataclass
class MangaInfo:
    id: str
    title: str = field(default_factory=str)
    altTitles: list[str] = field(default_factory=list)
    description: str = field(default_factory=str)
    lastVolume: str = field(default_factory=str)
    lastChapter: str = field(default_factory=str)
    status: str = field(default_factory=str)
    genres: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    cover_art: str = field(default_factory=str)

    def fetch(self):
        url = f"https://api.mangadex.org/manga/{self.id}?includes[]=cover_art"
        res = requests.get(url)

        if res.status_code != 200:
            print(f"No manga with id: '{self.id}' is found!")
            exit(0)

        json_res = res.json()

        data = json_res["data"]
        attributes: dict = data["attributes"]

        self.title = attributes["title"]["en"]
        alt_titles: list[dict[str, str]] = attributes["altTitles"]

        for alt_t in alt_titles:
            # Append the value of the first key
            self.altTitles.append(alt_t[list(alt_t.keys())[0]])

        self.description = attributes["description"]["en"]
        self.lastVolume = attributes["lastVolume"]
        self.lastChapter = attributes["lastChapter"]
        self.status = attributes["status"]

        tags: list[dict] = attributes["tags"]

        for tag in tags:
            tag_attr = tag["attributes"]
            name = tag_attr["name"]["en"]
            group = tag_attr["group"]

            if group == "genre":
                self.genres.append(name)
            elif group == "theme":
                self.themes.append(name)

        rela_list: list[dict] = data["relationships"]

        for rela in rela_list:
            rela_type = rela["type"]

            if rela_type != "cover_art":
                continue

            if rela["attributes"]:
                low_res = False
                file_name = rela["attributes"]["fileName"]

                if low_res:
                    file_name += ".256.jpg"

                self.cover_art = f"https://mangadex.org/covers/{self.id}/{file_name}"

        return self


@dataclass
class Page:
    num: int = field(default_factory=int)
    url: str = field(default_factory=str)
    file_name: str = field(default_factory=str)


def fetch_pages(chapter_id: str) -> list[Page]:
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}?forcePort443=false"

    res = requests.get(url)

    res_json = res.json()

    pages = []

    chapter = res_json["chapter"]
    hash = chapter["hash"]
    data = chapter["data"]

    for filename in data:
        page_url = f"https://uploads.mangadex.org/data/{hash}/{filename}"
        parsed_filename = parse_filename(filename)
        new_page = Page(int(parsed_filename[0]), page_url, parsed_filename[1])

        pages.append(new_page)

    return pages


@dataclass
class Chapter:
    id: str
    volume: str
    number: str
    title: str


def fetch_chapters(manga_id) -> list[Chapter]:
    print("Fetching chapters")
    offset: int = 0
    limit: int = 96
    chapters = []

    while True:
        url = f"https://api.mangadex.org/manga/{manga_id}/feed?translatedLanguage[]=en&limit={limit}&order[volume]=asc&order[chapter]=asc&offset={offset}"
        res = requests.get(url)

        json_res = res.json()
        data: list = json_res["data"]

        # If data is empty that means we reached the end of manga
        if len(data) == 0:
            break

        print("Fetching chapters")

        for chapter in data:
            id = chapter["id"]
            ch_type = chapter["type"]

            if ch_type != "chapter":
                continue

            attr = chapter["attributes"]

            volume = attr["volume"]
            num = attr["chapter"]
            title = attr["title"]

            if attr["externalUrl"]:
                continue

            new_chapter = Chapter(id, volume, num, title)

            chapters.append(new_chapter)

        offset = offset + limit
        time.sleep(0.600)

    return chapters


class Manga:
    def __init__(self, id: str):
        self.id = id
        self.info: MangaInfo = MangaInfo(id).fetch()
        self.chapters: list[Chapter] = fetch_chapters(id)


def main(manga_id: str):
    manga = Manga(manga_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--id", type=str, required=True, help="ID of manga you want to download."
    )

    args = parser.parse_args()

    main(args.id)
