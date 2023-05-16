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

#### _GitHub Action:_

```yaml
      - uses: docker://ghcr.io/chipwolf/generate-badges:latest
        with:
          format: markdown # default
          id: default # default
          output: README.md
          slugs: |
            osu
            github
            americanexpress
            nodered
            opensea
          sort: 'hilbert' # default
          style: 'for-the-badge' # default
```

#### _CLI:_

```bash
$ python3 icons.py -s osu github americanexpress nodered opensea
```

#### _Output:_

<!-- start chipwolf/generate-badges default -->
[![BadgeSort](https://img.shields.io/badge/BadgeSort-000000.svg?style=for-the-badge&logo=githubsponsors)](https://github.com/ChipWolf/generate-badges)
![GitHub](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=github&logoColor=white)
![Node-RED](https://img.shields.io/badge/Node--RED-8F0000.svg?style=for-the-badge&logo=nodered&logoColor=white)
![osu!](https://img.shields.io/badge/osu%21-FF66AA.svg?style=for-the-badge&logo=osu&logoColor=white)
![OpenSea](https://img.shields.io/badge/OpenSea-2081E2.svg?style=for-the-badge&logo=opensea&logoColor=white)
![American Express](https://img.shields.io/badge/American%20Express-2E77BC.svg?style=for-the-badge&logo=americanexpress&logoColor=white)
<!-- end chipwolf/generate-badges default -->

---

### Generate five random badges:

#### _GitHub Action:_

```yaml
      - uses: docker://ghcr.io/chipwolf/generate-badges:latest
        with:
          id: foobar
          format: html
          output: README.md
          random: 5
          sort: 'false'
          style: flat-square
```

#### _CLI:_

```bash
$ python3 icons.py -i foobar -s false -r 5 -f html -b flat-square
```

#### _Output:_

<!-- start chipwolf/generate-badges foobar -->
<p>
  <a href="#"><img alt="Pegasus Airlines" src="https://img.shields.io/badge/Pegasus%20Airlines-FDC43E.svg?style=flat-square&logo=pegasusairlines&logoColor=black"></a>
  <a href="#"><img alt="CBS" src="https://img.shields.io/badge/CBS-033963.svg?style=flat-square&logo=cbs&logoColor=white"></a>
  <a href="#"><img alt="Snapcraft" src="https://img.shields.io/badge/Snapcraft-82BEA0.svg?style=flat-square&logo=snapcraft&logoColor=white"></a>
  <a href="#"><img alt="Observable" src="https://img.shields.io/badge/Observable-353E58.svg?style=flat-square&logo=observable&logoColor=white"></a>
  <a href="#"><img alt="Oh Dear" src="https://img.shields.io/badge/Oh%20Dear-FFFFFF.svg?style=flat-square&logo=ohdear&logoColor=black"></a>
  <a href="https://github.com/ChipWolf/generate-badges"><img alt="BadgeSort" src="https://img.shields.io/badge/BadgeSort-000000.svg?style=flat-square&logo=githubsponsors"></a>
</p>
<!-- end chipwolf/generate-badges foobar -->

---

### Generate badges from a list of slugs, sorting using an inverted algorithm:

#### _GitHub Action:_

```yaml
      - uses: docker://ghcr.io/chipwolf/generate-badges:latest
        with:
          args: '--hue-rotate 240'
          id: example
          format: html
          output: README.md
          sort: 'step_invert'
          style: flat
          slugs: |
            angular,apollographql,brave,d3dotjs,docker
            git,githubactions,googlecloud,graphql,heroku
            html5,insomnia,mongodb,nestjs,nodedotjs
            npm,prettier,react,reactivex,redux
            rollupdotjs,sass,styledcomponents,typescript,webpack
```

#### _CLI:_

```bash
$ python3 icons.py -i example -c step_invert -o README.md -f html -b flat-square --hue-rotate 240 -s \
    angular,apollographql,brave,d3dotjs,docker, \
    git,githubactions,googlecloud,graphql,heroku, \
    html5,insomnia,mongodb,nestjs,nodedotjs, \
    npm,prettier,react,reactivex,redux, \
    rollupdotjs,sass,styledcomponents,typescript,webpack
```

#### _Output:_

<!-- start chipwolf/generate-badges example -->
<p>
  <a href="#"><img alt="D3.js" src="https://img.shields.io/badge/D3.js-F9A03C.svg?style=flat&logo=d3dotjs&logoColor=white"></a>
  <a href="#"><img alt="Prettier" src="https://img.shields.io/badge/Prettier-F7B93E.svg?style=flat&logo=prettier&logoColor=black"></a>
  <a href="#"><img alt="Node.js" src="https://img.shields.io/badge/Node.js-339933.svg?style=flat&logo=nodedotjs&logoColor=white"></a>
  <a href="#"><img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-47A248.svg?style=flat&logo=mongodb&logoColor=white"></a>
  <a href="#"><img alt="Webpack" src="https://img.shields.io/badge/Webpack-8DD6F9.svg?style=flat&logo=webpack&logoColor=black"></a>
  <a href="#"><img alt="React" src="https://img.shields.io/badge/React-61DAFB.svg?style=flat&logo=react&logoColor=black"></a>
  <a href="#"><img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6.svg?style=flat&logo=typescript&logoColor=white"></a>
  <a href="#"><img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=githubactions&logoColor=white"></a>
  <a href="#"><img alt="Google Cloud" src="https://img.shields.io/badge/Google%20Cloud-4285F4.svg?style=flat&logo=googlecloud&logoColor=white"></a>
  <a href="#"><img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=docker&logoColor=white"></a>
  <a href="#"><img alt="Redux" src="https://img.shields.io/badge/Redux-764ABC.svg?style=flat&logo=redux&logoColor=white"></a>
  <a href="#"><img alt="Apollo GraphQL" src="https://img.shields.io/badge/Apollo%20GraphQL-311C87.svg?style=flat&logo=apollographql&logoColor=white"></a>
  <a href="#"><img alt="Insomnia" src="https://img.shields.io/badge/Insomnia-4000BF.svg?style=flat&logo=insomnia&logoColor=white"></a>
  <a href="#"><img alt="Heroku" src="https://img.shields.io/badge/Heroku-430098.svg?style=flat&logo=heroku&logoColor=white"></a>
  <a href="#"><img alt="GraphQL" src="https://img.shields.io/badge/GraphQL-E10098.svg?style=flat&logo=graphql&logoColor=white"></a>
  <a href="#"><img alt="ReactiveX" src="https://img.shields.io/badge/ReactiveX-B7178C.svg?style=flat&logo=reactivex&logoColor=white"></a>
  <a href="#"><img alt="Sass" src="https://img.shields.io/badge/Sass-CC6699.svg?style=flat&logo=sass&logoColor=white"></a>
  <a href="#"><img alt="styled-components" src="https://img.shields.io/badge/styled--components-DB7093.svg?style=flat&logo=styledcomponents&logoColor=white"></a>
  <a href="#"><img alt="Brave" src="https://img.shields.io/badge/Brave-FB542B.svg?style=flat&logo=brave&logoColor=white"></a>
  <a href="#"><img alt="Git" src="https://img.shields.io/badge/Git-F05032.svg?style=flat&logo=git&logoColor=white"></a>
  <a href="#"><img alt="rollup.js" src="https://img.shields.io/badge/rollup.js-EC4A3F.svg?style=flat&logo=rollupdotjs&logoColor=white"></a>
  <a href="#"><img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=html5&logoColor=white"></a>
  <a href="#"><img alt="npm" src="https://img.shields.io/badge/npm-CB3837.svg?style=flat&logo=npm&logoColor=white"></a>
  <a href="#"><img alt="NestJS" src="https://img.shields.io/badge/NestJS-E0234E.svg?style=flat&logo=nestjs&logoColor=white"></a>
  <a href="#"><img alt="Angular" src="https://img.shields.io/badge/Angular-DD0031.svg?style=flat&logo=angular&logoColor=white"></a>
  <a href="https://github.com/ChipWolf/generate-badges"><img alt="BadgeSort" src="https://img.shields.io/badge/BadgeSort-000000.svg?style=flat&logo=githubsponsors"></a>
</p>
<!-- end chipwolf/generate-badges example -->
