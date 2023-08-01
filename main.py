import requests
import argparse
from dataclasses import dataclass, field


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


class Manga:
    def __init__(self, id: str):
        self.id = id
        self.info = MangaInfo(id).fetch()


def main(manga_id: str):
    manga = Manga(manga_id)

    print(manga.info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--id", type=str, required=True, help="ID of manga you want to download."
    )

    args = parser.parse_args()

    main(args.id)
