# How to download in bulk from mangadex.org

## 1. get the id of any manga

for example: https://mangadex.org/title/a460ab18-22c1-47eb-a08a-9ee85fe37ec8/bleach-digital-colored-comics
the manga id is: a460ab18-22c1-47eb-a08a-9ee85fe37ec8

hit this endpoint to get info about the manga
`https://api.mangadex.org/manga/{MANGA_ID}`

Example response for `https://api.mangadex.org/manga/a460ab18-22c1-47eb-a08a-9ee85fe37ec8`

[Example response](./example-res/manga.json)

to get list of volumes hit this endpoint
`https://api.mangadex.org/manga/{MANGA_ID}/aggregate?translatedLanguage[]=en`

Example response for `https://api.mangadex.org/manga/a460ab18-22c1-47eb-a08a-9ee85fe37ec8/aggregate?translatedLanguage[]=en`

[Example response](./example-res/aggregate.json)

to get the pages for the chapter hit this endpoint
`https://api.mangadex.org/at-home/server/{CHAPTER_ID}?forcePort443=false`

Example response for `https://api.mangadex.org/at-home/server/bc9dfc26-a53a-4e96-96c1-21ee4777cbef?forcePort443=false`

[Example response](./example-res/pages.json)

from the response extract chapter.hash and chapter.data

to get the image hit this endpoint
`https://uploads.mangadex.org/data/{CHAPTER.HASH}/{CHAPTER.DATA[INDEX]}`
