#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from hilbert import Hilbert_to_int
from simpleicons.all import icons
from urllib.parse import quote

import argparse
import logging
import random
import requests
import sys
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Generates branded badges with Shields.io and SimpleIcons.org.')
parser.add_argument('-b', '--badge-style', type=str, default='for-the-badge', help='Shields.io badge style.')
parser.add_argument('-f', '--format', type=str, default='markdown', help='Output format (markdown/html).')
parser.add_argument('-i', '--id', type=str, default='default', help='Badge generation ID.')
parser.add_argument('-n', '--no-hilbert', action='store_true', help='Do not sort badges by color using a Hilbert walk.')
parser.add_argument('-r', '--random', type=int, default=1, help='Number of random icons to generate.')
parser.add_argument('-s', '--slugs', nargs='+', default='', help='SimpleIcons.org slugs to use.')
parser.add_argument('-v', '--verify', action='store_true', help='Verify the generated badge is valid by requesting it from Shields.io.')
parser.add_argument('-o', '--output', type=str, default='', help='Output file name.')
args, unknown = parser.parse_known_args()
logger.debug(args)

# user provided slugs
if len(args.slugs) > 0:
    slugs = args.slugs
    # check if slugs provided exist at SimpleIcons.org
    for slug in list(set(slugs)):
        if slug not in icons:
            logger.fatal('Slug %s not found at SimpleIcons.org. Exiting.' % slug)
            sys.exit(1)
    logger.info('Generating badges from slugs: %s...' % ', '.join(list(set(args.slugs))))
# user requested a random list of slugs of length args.random
elif args.random > 0:
    slugs = random.sample(list(icons), args.random)
    logger.info('Generating %d random badges...' % args.random)
# user requested all slugs
elif args.random < 0:
    slugs = list(set(icons))
    logger.info('Generating all badges...')
# user did not provide a required argument
else:
    logger.fatal('No slugs or random icons specified. Exiting.')
    sys.exit(1)

icon_base = 'https://img.shields.io/badge'
icon_list = []

# generate Shields.io URLs for each slug
for slug in slugs:
    logger.debug('slug: %s' % slug)
    icon = icons.get(slug)
    icon_title_safe = quote(icon.title.encode('utf8'), safe='').replace('-', '--')
    icon_rgb = [int(icon.hex[0:2], 16), int(icon.hex[2:4], 16), int(icon.hex[4:6], 16)]
    icon_brightness = (icon_rgb[0] * 299 + icon_rgb[1] * 587 + icon_rgb[2] * 114) / 255000
    icon_hex_comp = 'white' if icon_brightness <= 0.7 else 'black'
    icon_url = f'{icon_base}/{icon_title_safe}-{icon.hex}.svg'
    icon_url += f'?style={args.badge_style}&logo={icon.slug}&logoColor={icon_hex_comp}'
    icon_list.append({ 'rgb': icon_rgb, 'slug': icon.slug, 'title': icon.title, 'url': icon_url })

# sort the icons by Hilbert walk
if not args.no_hilbert:
    logger.debug('Sorting icons by color using a Hilbert walk...')
    icon_list.sort(key=lambda c:Hilbert_to_int(c['rgb']))

badges = ''

# enumerate all icons and generate badges
for icon in icon_list:
    try:
        logger.debug(icon)

        # verify the badge is valid by requesting it from Shields.io
        if args.verify:
            r = requests.get(icon['url'])
            if r.status_code != 200:
                logger.debug(r.text)
                logger.fatal('Badge verification failed for %s. Exiting.' % icon['slug'])
                sys.exit(1)

        # generate the badge markup depending on the output format
        if args.format == 'markdown':
            badges += f'![{icon["title"]}]({icon["url"]})\n'
        elif args.format == 'html':
            badges += f'  <a href="#"><img alt="{icon["title"]}" src="{icon["url"]}"></a>\n'
        else:
            logger.fatal('Unknown output format: %s. Exiting.' % args.format)
            sys.exit(1)

    except Exception as e:
        logger.fatal('Error generating badge for %s. Exiting.' % icon['slug'])
        sys.exit(1)

# wrap badges in <p> tags if outputting HTML
if args.format == 'html':
    badges = '<p>\n' + badges + '</p>\n'

# wrap badges with a header and footer
badges_header = f'<!-- start chipwolf/generate-badges {args.id} -->\n'
badges_footer = f'<!-- end chipwolf/generate-badges {args.id} -->\n'
badges = badges_header + badges + badges_footer

# if output file is specified, write badges to file
if args.output:
    with open(args.output, 'r') as f:
        output_content = f.read()
    # replace existing badges between the badge header and footer with the new ones
    output_content = re.sub(fr"{badges_header}.*?{badges_footer}", f'{badges}', output_content, flags=re.S)
    # write the output file
    with open(args.output, 'w') as f:
        f.write(output_content)
# otherwise, print badges to stdout
else:
    try:
        print(badges)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(badges.encode('utf8').decode(sys.stdout.encoding))
        else:
            print(badges.encode('utf8'))

logger.info('Done.')
sys.exit(0)
