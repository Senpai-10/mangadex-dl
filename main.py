import requests
import argparse
import time
import os
from dataclasses import dataclass, field
from slugify import slugify


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
    cover_art_file_ext: str = field(default_factory=str)

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
                self.cover_art_file_ext = file_name.split(".")[1] or "png"

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


def fetch_chapters(
    manga_id, download_list_volumes: list[str], download_list_chapters: list[str]
) -> list[Chapter]:
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
            title = attr["title"] or "untitled"

            if attr["externalUrl"]:
                continue

            if not "*" in download_list_volumes and not volume in download_list_volumes:
                continue
            if not "*" in download_list_chapters and not num in download_list_chapters:
                continue

            new_chapter = Chapter(id, volume, num, title)

            chapters.append(new_chapter)

        offset = offset + limit
        time.sleep(0.600)

    return chapters


class Manga:
    def __init__(
        self,
        id: str,
        download_list_volumes: list[str],
        download_list_chapters: list[str],
        output_dir: str,
    ):
        self.id = id
        self.output_dir = output_dir
        self.info: MangaInfo = MangaInfo(id).fetch()
        self.chapters: list[Chapter] = fetch_chapters(
            id, download_list_volumes, download_list_chapters
        )

    def download(self):
        manga_dir = os.path.join(self.output_dir, slugify(self.info.title))

        if not os.path.exists(manga_dir):
            os.makedirs(manga_dir)

        cover_art_path = os.path.join(
            manga_dir, f"cover.{self.info.cover_art_file_ext}"
        )

        # Download the cover_art
        if not os.path.exists(cover_art_path):
            with open(cover_art_path, "wb") as f:
                f.write(requests.get(self.info.cover_art).content)

        # TODO: dump self.info in a json file called "info.json"

        volumes_dir = os.path.join(manga_dir, "volumes")

        if not os.path.exists(volumes_dir):
            os.makedirs(volumes_dir)

        # Download chapters
        for chapter in self.chapters:
            volume_dir = os.path.join(volumes_dir, chapter.volume)

            if not os.path.exists(volume_dir):
                os.makedirs(volume_dir)

            new_chapter_title = slugify(chapter.title).replace("-", " ")

            chapter_dir = os.path.join(
                volume_dir,
                f"{chapter.number} {new_chapter_title}",
            )

            if not os.path.exists(chapter_dir):
                os.makedirs(chapter_dir)


def dir_path(s):
    if os.path.isdir(s):
        return os.path.normpath(s)
    else:
        os.makedirs(os.path.normpath(s))
        return os.path.normpath(s)


def expand_range(s: str) -> list[str]:
    l = []
    start, end = s.split("-")

    if not start.isdigit() or not end.isdigit():
        return []

    for i in range(int(start), int(end) + 1):
        l.append(str(i))

    return l


def parse_download_limit(s: str):
    # NOTE: Needs refactoring
    l = []
    list_of_nums: list[str] | None = None

    if "," in s:
        list_of_nums = s.split(",")
    elif not "," in s and " " in s:
        list_of_nums = s.split(" ")

    if list_of_nums:
        for n in list_of_nums:
            n = n.strip()

            if not n:
                continue

            if "-" in n:
                for r in expand_range(n):
                    l.append(r)
            else:
                l.append(n)
    else:
        if "-" in s:
            for r in expand_range(s):
                l.append(r)
        else:
            return [s]

    if not s or len(l) == 0:
        return ["*"]

    return l


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--id", type=str, required=True, help="ID of manga you want to download."
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=dir_path,
        default=os.getcwd(),
        help="Output directory for downloaded manga",
    )

    parser.add_argument(
        "-v",
        "--volumes",
        type=str,
        default="*",
        help="Volumes to donwload, can be a range or a '*' to download all volumes (Default: '*') Example: \"--volumes '1,2,3,4,5-10'\" or \"--volumes '1-10'\" or \"--volumes '*'\"",
    )

    parser.add_argument(
        "-c",
        "--chapters",
        type=str,
        default="*",
        help="Chapters to donwload, can be a range or a '*' to download all chapters (Default: '*') Example: \"--chapters '1,2,3,4,5-10'\" or \"--chapters '1-10'\" or \"--chapters '*'\"",
    )

    args = parser.parse_args()

    download_list_volumes = parse_download_limit(args.volumes)
    download_list_chapters = parse_download_limit(args.chapters)

    manga = Manga(
        args.id, download_list_volumes, download_list_chapters, args.output_dir
    )

    manga.download()
