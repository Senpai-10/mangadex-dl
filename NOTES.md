# How to download in bulk from mangadex.org

## 1. Get id manga

for example: https://mangadex.org/title/a460ab18-22c1-47eb-a08a-9ee85fe37ec8/bleach-digital-colored-comics
the manga id is: a460ab18-22c1-47eb-a08a-9ee85fe37ec8

## 2. Get info about the manga

`https://api.mangadex.org/manga/{MANGA_ID}`

Example response for `https://api.mangadex.org/manga/a460ab18-22c1-47eb-a08a-9ee85fe37ec8`

[Example response](./example-res/manga.json)

## 3. Get list of volumes

`https://api.mangadex.org/manga/{MANGA_ID}/aggregate?translatedLanguage[]=en`

Example response for `https://api.mangadex.org/manga/a460ab18-22c1-47eb-a08a-9ee85fe37ec8/aggregate?translatedLanguage[]=en`

[Example response](./example-res/aggregate.json)

## 4. Get the pages for the chapter

`https://api.mangadex.org/at-home/server/{CHAPTER_ID}?forcePort443=false`

Example response for `https://api.mangadex.org/at-home/server/bc9dfc26-a53a-4e96-96c1-21ee4777cbef?forcePort443=false`

[Example response](./example-res/pages.json)

## 5. Download pages of a chapter

from the last response extract chapter.hash and chapter.data

chapter.data is an array

```python
for image in chapter.data:
    print(f"page: https://uploads.mangadex.org/data/{chapter.hash}/{image}")
```

Output:

```text
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/1-a5e9c12679b341d615712051321d4b2d7789bdae0853d3e6761e07a93fb06bf8.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/2-9a02cb69c8af42c2e0017b4b2652a4a516bdc041c11b0fc229fee057cbce780c.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/3-273c3a4aa7f8481ca5612e1f37050dc95c9c6998929f71f4e03a489ae5058b6f.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/4-edb22e2c77fb87701782e6cf134c93a5dadbf87a18b9d575dd1e4c239bb5bdb4.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/5-86e9bed1d013507634b2a997ab5c0036508c62b16c5b44a311921ede1463ea74.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/6-b2b258bfc618b1f594fefb11f89f705726849ae5908c5d0e39d32087fa914c26.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/7-dd53cf2222319d28468c4276ea7ead90e18013f74ea1b57a0e3110e585f318cd.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/8-66a3cc1929b1df05349b985d4c236c9ac51367ebb4f06c72b8477c63d9694a37.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/9-2832a0b3cc8d704ca471c0224a20ba10ca7ffdc7b728bc299d082895b5249264.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/10-2b9395c98fa82e1f2374b0ddd1255d0ba8f03daf0ad9584a5480840ce8e1395a.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/11-2ca50f9019da90dc838400a1cf383d991a66992958347b57f03429d35ea0d813.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/12-b57e70b27448ddc0e1659533b8396e1b996a1dd917678a777087246afa21d948.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/13-8721066fce2bbff67913e98eef150e1e83e696f403a4b6caeab85599a55361c7.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/14-cdbc862a12e92e1c6ea64057be8441068b6b76ef53ae6420df5427a133122602.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/15-1e23241b219a3b9bfce1d6d66e427ce6e642240d2b001fb6b2b23751f0eb84d5.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/16-5ea1898a138868bf986cf850cb0303abdec4e5c5a492e102cf1974941e0ce54a.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/17-d06cf7208acf7f83b0fe05e25264d1e93f46305a1de2606bd01c15010fe33aec.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/18-6e981b590749983ac377467cfb6ae207086fadbaac53e1c5d7a33a314338579c.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/19-f13c21f636f0bb80b54fa251f82014eac28b80af04d2775ea5358b33204f9d5c.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/20-4f4b4184ad1f495eba535602b9d2819974801500fea6d673e48d5e8768b79fb9.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/21-6d127f1c8674ebbf044e7c6a12087a8c3a28600afb42657acc9f6ab0f303e12b.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/22-18d1052b596f9379b0aaa098d67b130fe8b74edf464ad0d6d11f50badd986d46.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/23-d4b8f27dea45dff3af85c13236683c7144bd518fea6662e9dec7bc1196f32893.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/24-d7949d5c17958f310a81eb06c9be7849e33b72b5ee19de7f78e5e9d57b1b8430.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/25-730da8469cabb3ea426ef8f0c8c6261f7f79cabc9f9a5ef56f1e4f8dece71a84.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/26-36b9142676eb6b4846d14c5f91bb6169671bd64370678285a7d2b6e9540121a4.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/27-77a7e2a0c79783a2a706c9f804c8c4a7c96f1bd08567f703c776fff0b0001068.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/28-759d9c53b2f8aa0bb3a3ca85b0edc9cdc3da4559dfdaac8d5f52bcacb6060793.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/29-12b61d95a397279aa4aef18e7faba4aa4a885e298af24f88576d0cfa0c2db6fd.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/30-d84f2a39bcb6c8d6e5e7e09c890044ab8c2b9b0b6454b2dbbbad25aaac32bb18.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/31-b39a48302b8a72e2ac380adea37f56b75bb94aa8cc1d0828e4ee8e0d3193afe4.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/32-d0c143cfab3928f037cbc9d563875af2b13a4033b1fad906897ff69e4df5c6ab.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/33-48d7534f5520dd6a18c2b7373159113f7d3e5e4784038a4a64afe2eaa17ce03d.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/34-b4b6e8a23afafb72a82605ae0e6f91e15694588f20cf2a5ec65483ef2bf64423.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/35-8b40587ec8ead57013f95e5ff5294ab762d0b130fe74ad6d36b2da019161fc7e.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/36-3d32a1f9572b51da5009df694d738888fa629b1abd3e7c5cbe08cc8e7511e1ea.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/37-3bab778cb6971e81bb12fa8dcc7f2a47fc7f796f5b475c6a816f030d218166a5.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/38-a2a3e6b87edbd2d9242d7aaed1e801948b8738ff1014174c3a585fc50304a300.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/39-f83ad2d686b266847471a8a74323450dc891b668d386574e85964ced3a1f7379.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/40-5aa52f2883961853fc238113841e3e6a682d5992ca398aaaf6bc40df5c59fd32.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/41-79dd5c6aa8dd9d83c2584b34dc777c60b501870a4621c6fa01e069d7d1613eb8.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/42-f07190d6c1dbea485a9ac2e458098d716b687a8197c6f28637f05134509ccd23.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/43-b90b8d228bbc1ee096a24473c925330be583dc7bd3e6ebda677fbee3d1d519ec.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/44-f6787f1a5958c71206b43860452f428374108ee958e21f13f6a2ddbb3de02788.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/45-fee42d98f02b22ce354da662921af50b7736fd19e37dddc8402257fa756cac80.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/46-5b6691326b516136012d59f4ed968462dbb9d1e933fd29e3aa688664dacc4a32.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/47-b38de6450557d39a6070aabf7126b8901c1943da19668622c18b14f2043d2e11.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/48-0988038f8577616a79f97a9b28352df6e35217b41b58a018a02e4b54a8fb5d60.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/49-088bd5dd686cb6fdc63c0ad90cd268c7a11b845279127108e11416aa3614f592.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/50-9aa73dbcc17d475c73ffefa7f343f36569152fb7de786b5219d1739d09204dc7.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/51-4e8c9e4181ccc7cfb9597f1f2ab9f7dff0179a29552a678b6b53dd3b15a41ab5.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/52-a2e75d26fab528472b5134c401e108758b0ca58a07f43a39236e927cdd4a72f0.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/53-2c9bbfcf67c650e3cf194582d6f981d37b064a7cf2a753ee29dba2d973355a48.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/54-9dab0e58ad4c1fbbd157fb3e5db8848ec9f56fd5d7834a7b5a1a3c8c88888bb3.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/55-ae96a4ef31dde468eeacf6c674ac536e0a53bf1f9231422fd6008138b5c38c26.jpg
https://uploads.mangadex.org/data/779edf22cefbd20cceec328ccca7a3d1/56-c7af3399f2cf4c1dbf539783ae9d09f22fbf0c6e31527539aa8d5b37a24bf989.jpg
```
