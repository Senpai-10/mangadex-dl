# How to download in bulk from mangadex.org

## 1. Get id manga

Example: `https://mangadex.org/title/239d6260-d71f-43b0-afff-074e3619e3de/bleach`
The manga id is: `239d6260-d71f-43b0-afff-074e3619e3de`

## 2. Get info about the manga

Endpoint: `https://api.mangadex.org/manga/{MANGA_ID}?includes[]=cover_art`

Example: `https://api.mangadex.org/manga/239d6260-d71f-43b0-afff-074e3619e3de?includes[]=cover_art`

### 2.1 Get cover art

in relationships type "cover_art" extract attributes.fileName

if you want the cover art to be of size 256
just append ".256.jpg" at the end of fileName

the image url is `https://mangadex.org/covers/{MANGA_ID}/{FILE_NAME}`

## 3. Get list of volumes

Endpoint: `https://api.mangadex.org/manga/{MANGA_ID}/feed?translatedLanguage[]=en&limit=96&order[volume]=asc&order[chapter]=asc&offset=0`

Example: `https://api.mangadex.org/manga/239d6260-d71f-43b0-afff-074e3619e3de/feed?translatedLanguage[]=en&limit=96&order[volume]=asc&order[chapter]=asc&offset=0`

offset 0 is the first page

if you want to get the next page
add the limit to offset value

```python
offset = offset + limit
```

If data is empty that means

## 4. Get the pages for a chapter

Endpoint: `https://api.mangadex.org/at-home/server/{CHAPTER_ID}?forcePort443=false`

Example: `https://api.mangadex.org/at-home/server/37d6949a-c7ce-4855-b838-4fd572e87629?forcePort443=false`

## 5. Download pages of a chapter

from the last response extract chapter.hash and chapter.data

chapter.data is an array

```python
for image in chapter.data:
    print(f"page: https://uploads.mangadex.org/data/{chapter.hash}/{image}")
```

Example output:

```text
https://uploads.mangadex.org/data/{ID}/1-a5e9c12679b341d615712051321d4b2d7789bdae0853d3e6761e07a93fb06bf8.jpg
...
https://uploads.mangadex.org/data/{ID}/55-ae96a4ef31dde468eeacf6c674ac536e0a53bf1f9231422fd6008138b5c38c26.jpg
https://uploads.mangadex.org/data/{ID}/56-c7af3399f2cf4c1dbf539783ae9d09f22fbf0c6e31527539aa8d5b37a24bf989.jpg
```
