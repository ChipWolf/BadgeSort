#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from urllib.parse import quote
from colorsys import rgb_to_hsv

import argparse
import base64
import logging
import math
import random
import sys
import re
import requests
import tempfile
import os
import subprocess

from simpleicons.all import icons
from .hilbert import Hilbert_to_int

# Cache for logo availability checks to avoid repeated requests
_logo_availability_cache = {}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def svg_to_base64_data_uri(svg_content, fill_color='white'):
    """Convert an SVG to a base64-encoded data URI with specified fill color."""
    # Add fill color to the path element
    # Simple Icons SVGs typically have a single <path> element
    svg_with_fill = svg_content.replace('<path ', f'<path fill="{fill_color}" ')
    
    # Encode to base64
    svg_bytes = svg_with_fill.encode('utf-8')
    base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    
    # Return as data URI
    return f'data:image/svg+xml;base64,{base64_svg}'

def run(args):
    # user provided slugs
    if len(args.slugs) > 0:
        slugs = ','.join(args.slugs).split(',')
        slugs[:] = [slug for slug in slugs if slug != '']
        # check if slugs provided exist
        for slug in list(set(slugs)):
            if slug not in icons:
                logger.info(f'Slug %s not found in package simpleicons.' % slug)
                slugs.remove(slug)
        logger.info('Generating badges from slugs: %s...' % ', '.join(list(set(slugs))))
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

    icon_base = 'https://img.shields.io/badge' if args.provider == 'shields' else 'https://badgen.net/badge'
    icon_list = []

    # generate badge URLs for each slug
    for slug in slugs:
        logger.debug('slug: %s' % slug)
        icon = icons.get(slug)
        icon_title_safe = quote(icon.title.encode('utf8'), safe='').replace('-', '--')
        icon_rgb = [int(icon.hex[0:2], 16), int(icon.hex[2:4], 16), int(icon.hex[4:6], 16)]
        icon_brightness = (icon_rgb[0] * 299 + icon_rgb[1] * 587 + icon_rgb[2] * 114) / 255000
        icon_hex_comp = 'white' if icon_brightness <= 0.7 else 'black'
        
        if args.provider == 'shields':
            # Shields.io format
            icon_url = f'{icon_base}/{icon_title_safe}-{icon.hex}.svg'
            icon_url += f'?style={args.badge_style}&logo={icon.slug}&logoColor={icon_hex_comp}'
        else:
            # Badgen.net format
            # Convert SVG to base64 data URI with adaptive color based on background luminosity
            icon_data_uri = svg_to_base64_data_uri(icon.svg, icon_hex_comp)
            icon_data_uri_encoded = quote(icon_data_uri, safe='')
            icon_url = f'{icon_base}/icon/{icon_title_safe}?icon={icon_data_uri_encoded}&label&color={icon.hex}&labelColor={icon.hex}'
        
        icon_list.append({ 'rgb': icon_rgb, 'slug': icon.slug, 'title': icon.title, 'url': icon_url })

    if args.no_thanks is True:
        if args.provider == 'shields':
            icon_url = f'{icon_base}/BadgeSort-000000.svg'
            icon_url += f'?style={args.badge_style}&logo=githubsponsors'
        else:
            # Badgen with githubsponsors heart icon
            # Use the githubsponsors icon with adaptive color based on luminosity
            sponsor_icon = icons.get('githubsponsors')
            # Black background has rgb [0,0,0], brightness = 0
            # We want white icon on black background
            badge_rgb = [0, 0, 0]
            badge_brightness = (badge_rgb[0] * 299 + badge_rgb[1] * 587 + badge_rgb[2] * 114) / 255000
            icon_color = 'white' if badge_brightness <= 0.7 else 'black'
            
            # Convert the githubsponsors SVG to data URI with adaptive color
            sponsor_data_uri = svg_to_base64_data_uri(sponsor_icon.svg, icon_color)
            sponsor_data_uri_encoded = quote(sponsor_data_uri, safe='')
            icon_url = f'{icon_base}/icon/BadgeSort?icon={sponsor_data_uri_encoded}&label&color=000000&labelColor=000000'
        icon_list.append({ 'rgb': [0, 0, 0], 'slug': 'badgesort', 'title': 'BadgeSort', 'url': icon_url })

    def lum (r,g,b):
        return math.sqrt( .241 * r + .691 * g + .068 * b )

    def step (r,g,b, repetitions=1, rotate=0, invert=False):
        l = lum(r,g,b)
        h, s, v = rgb_to_hsv(r,g,b)
        h = (h + rotate / 255) % 1
        h2 = int(h * repetitions)
        v2 = int(v * repetitions)
        if h2 % 2 == 1 and invert:
            v2 = repetitions - v2
            l = repetitions - l
        return (h2, l, v2)

    # sort the icons by chosen method
    if args.color_sort == 'hilbert':
        logger.debug('Sorting icons by color using a Hilbert walk...')
        icon_list.sort(key=lambda c:Hilbert_to_int(c['rgb']))
    elif args.color_sort == 'hsv':
        logger.debug('Sorting icons by color using HSV...')
        icon_list.sort(key=lambda c:rgb_to_hsv(*c['rgb']))
    elif args.color_sort == 'random':
        logger.debug('Sorting icons randomly...')
        random.shuffle(icon_list)
    elif args.color_sort == 'step':
        logger.debug('Sorting icons by color using a step function...')
        icon_list.sort(key=lambda c:step(*c['rgb'], 8, args.hue_rotate))
    elif args.color_sort == 'step_invert':
        logger.debug('Sorting icons by color using an inverted step function...')
        icon_list.sort(key=lambda c:step(*c['rgb'], 8, args.hue_rotate, True))
    elif args.color_sort == 'luminance':
        logger.debug('Sorting icons by color using luminance...')
        icon_list.sort(key=lambda c:lum(*c['rgb']))

    # invert the list if args.hue_invert is set
    if args.reverse:
        icon_list.reverse()

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
                md_badge = f'![{icon["title"]}]({icon["url"]})'
                if icon["slug"] == 'badgesort':
                    badges += f'[{md_badge}](https://github.com/ChipWolf/BadgeSort)\n'
                else:
                    badges += md_badge + '\n'
            elif args.format == 'html':
                if icon["slug"] == 'badgesort':
                    badges += '  <a href="https://github.com/ChipWolf/BadgeSort">'
                else:
                    badges += '  <a href="#">'
                badges += f'<img alt="{icon["title"]}" src="{icon["url"]}"></a>\n'
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
    badges_header = f'<!-- start chipwolf/badgesort {args.id} -->\n'
    badges_footer = f'<!-- end chipwolf/badgesort {args.id} -->\n'
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

def main(raw_args=None):
    parser = argparse.ArgumentParser(description='Generates branded badges with Shields.io, Badgen.net and SimpleIcons.org.')
    parser.add_argument('-b', '--badge-style', type=str, default='for-the-badge', help='Shields.io badge style.')
    parser.add_argument('-c', '--color-sort', type=str, default='hilbert', help='Choose color sorting algorithm (hilbert/hsv/step/step_invert/luminance/random).')
    parser.add_argument('-f', '--format', type=str, default='markdown', help='Output format (markdown/html).')
    parser.add_argument('-i', '--id', type=str, default='default', help='Badge generation ID.')
    parser.add_argument('-p', '--provider', type=str, default='shields', help='Badge provider (shields/badgen).')
    parser.add_argument('-r', '--random', type=int, default=1, help='Number of random icons to generate.')
    parser.add_argument('-s', '--slugs', nargs='+', default='', help='SimpleIcons.org slugs to use.')
    parser.add_argument('-v', '--verify', action='store_true', help='Verify the generated badge is valid by requesting it from the badge provider.')
    parser.add_argument('-o', '--output', type=str, default='', help='Output file name.')
    parser.add_argument('--hue-rotate', type=int, default=0, help='Rotate the [step] generated icons hue sort by this many degrees.')
    parser.add_argument('--no-thanks', action='store_false', help='Hide the BadgeSort badge.')
    parser.add_argument('--reverse', action='store_true', help='Reverse the badges sort.')
    parser.add_argument('--embed-svg', action='store_true', help='Always embed SVG data URIs in Shields.io badges instead of using logo slugs.')
    parser.add_argument('--skip-logo-check', action='store_true', help='Skip checking if logos are missing from Shields.io (faster but may result in badges without icons).')
    args, unknown = parser.parse_known_args(raw_args)
    logger.debug(args)

    run(args)

    logger.info('Done.')
    sys.exit(0)

if __name__ == '__main__':
    main()
