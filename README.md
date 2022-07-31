# Generate and Sort Branded [Shields.io](https://shields.io) Badges by Color

**This is a Python 3 command-line tool and [GitHub Action](https://github.com/features/actions) automating the generation and color sorting of badges from [Shields.io](https://shields.io) that contain logos from [Simple Icons](https://simpleicons.org/).**

## Background:

Many [awesome GitHub profiles](https://github.com/abhisheknaiidu/awesome-github-profile-readme) contain a series of these badges to clearly indicate which tools, services, or other brands the user is affiliated with. These badge collections usually adopt the brand's color, icon, and name.

## The problem:

[Shields.io](https://shields.io) URLs for these badges are normally handcrafted or copypasta, following this rough format:

`https://img.shields.io/badge/<URL_ENCODED_BRAND_NAME>-<BRAND_HEX_COLOR>.svg?style=<BADGE_STYLE>&logoColor=<TEXT_HEX_COLOR>&logo=<SIMPLE_ICONS_SLUG>`

Normally, the user must repeat the process of manually rendering this URL for each badge they wish to display. This is what the result of this work might look like:

![Unsorted Badges](./.github/unsorted.png)

Then, if the user is inclined, they may spend additional time ordering the badges by color to make their profile more visually appealing:

![Sorted Badges](./.github/sorted.png)

This is a time consuming process if performed manually; it is difficult to maintain, hard to keep consistent, and makes future adjustments offputting.

## The solution:

This project automates the process of rendering out the badges into Markdown or HTML from a simple list of slugs.

The badges can be sorted by color _[as default]_ or left in the order specified.

![1D Hilbert sorted colors](./.github/hilbert.png)

> **Note**
> _Thanks to [this article](https://www.alanzucconi.com/2015/09/30/colour-sorting/) by **Alan Zucconi**, the visually appealing color sort is achived using a Hilbert walk._

## Examples:

### Generate five specific badges ordered by color:

#### GitHub Action:

```yaml
- uses: ChipWolf/generate-badges@v1
  with:
    format: markdown # default
    id: default # default
    slugs:
      - osu
      - github
      - americanexpress
      - nodered
      - opensea
    sort: true # default
```

#### CLI:

```bash
$ python3 icons.py -s osu github americanexpress nodered opensea
```

#### Output:

<!-- start chipwolf/generate-badges default -->
![GitHub](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=github&logoColor=white)
![Node-RED](https://img.shields.io/badge/Node--RED-8F0000.svg?style=for-the-badge&logo=nodered&logoColor=white)
![osu!](https://img.shields.io/badge/osu%21-FF66AA.svg?style=for-the-badge&logo=osu&logoColor=white)
![OpenSea](https://img.shields.io/badge/OpenSea-2081E2.svg?style=for-the-badge&logo=opensea&logoColor=white)
![American Express](https://img.shields.io/badge/American%20Express-2E77BC.svg?style=for-the-badge&logo=americanexpress&logoColor=white)
<!-- end chipwolf/generate-badges default -->

#### _Source:_

```markdown
<!-- start chipwolf/generate-badges default -->
![GitHub](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=github&logoColor=white)
![Node-RED](https://img.shields.io/badge/Node--RED-8F0000.svg?style=for-the-badge&logo=nodered&logoColor=white)
![osu!](https://img.shields.io/badge/osu%21-FF66AA.svg?style=for-the-badge&logo=osu&logoColor=white)
![OpenSea](https://img.shields.io/badge/OpenSea-2081E2.svg?style=for-the-badge&logo=opensea&logoColor=white)
![American Express](https://img.shields.io/badge/American%20Express-2E77BC.svg?style=for-the-badge&logo=americanexpress&logoColor=white)
<!-- end chipwolf/generate-badges default -->
```

---

### Generate five random badges:

#### GitHub Action:

```yaml
- uses: ChipWolf/generate-badges@v1
  with:
    id: foobar
    format: html
    random: 5
    sort: false
```

#### CLI:

```bash
$ python3 icons.py -n -r 5 -f html
```

#### Output:

<!-- start chipwolf/generate-badges foobar -->
<p>
  <a href="#"><img alt="Apache" src="https://img.shields.io/badge/Apache-D22128.svg?style=for-the-badge&logo=apache&logoColor=white"></a>
  <a href="#"><img alt="Roots Bedrock" src="https://img.shields.io/badge/Roots%20Bedrock-525DDC.svg?style=for-the-badge&logo=rootsbedrock&logoColor=white"></a>
  <a href="#"><img alt="Realm" src="https://img.shields.io/badge/Realm-39477F.svg?style=for-the-badge&logo=realm&logoColor=white"></a>
  <a href="#"><img alt="Microsoft PowerPoint" src="https://img.shields.io/badge/Microsoft%20PowerPoint-B7472A.svg?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white"></a>
  <a href="#"><img alt="Octane Render" src="https://img.shields.io/badge/Octane%20Render-000000.svg?style=for-the-badge&logo=octanerender&logoColor=white"></a>
</p>
<!-- end chipwolf/generate-badges foobar -->

#### _Source:_

```html
<!-- start chipwolf/generate-badges foobar -->
<p>
  <a href="#"><img alt="Apache" src="https://img.shields.io/badge/Apache-D22128.svg?style=for-the-badge&logo=apache&logoColor=white"></a>
  <a href="#"><img alt="Roots Bedrock" src="https://img.shields.io/badge/Roots%20Bedrock-525DDC.svg?style=for-the-badge&logo=rootsbedrock&logoColor=white"></a>
  <a href="#"><img alt="Realm" src="https://img.shields.io/badge/Realm-39477F.svg?style=for-the-badge&logo=realm&logoColor=white"></a>
  <a href="#"><img alt="Microsoft PowerPoint" src="https://img.shields.io/badge/Microsoft%20PowerPoint-B7472A.svg?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white"></a>
  <a href="#"><img alt="Octane Render" src="https://img.shields.io/badge/Octane%20Render-000000.svg?style=for-the-badge&logo=octanerender&logoColor=white"></a>
</p>
<!-- end chipwolf/generate-badges foobar -->
```
