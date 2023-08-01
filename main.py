import requests
import argparse


def main(manga_id: str):
    url = f"https://api.mangadex.org/manga/{manga_id}?includes[]=cover_art"
    res = requests.get(url)

    if res.status_code != 200:
        print(f"No manga with id: '{manga_id}' is found!")
        return

    json_res = res.json()

    print(json_res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--id", type=str, required=True, help="ID of manga you want to download."
    )

    args = parser.parse_args()

    main(args.id)
