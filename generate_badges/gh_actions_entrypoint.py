#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

from .icons import main

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug("Starting gh_actions_entrypoint.py")

    inputs = {}

    inputs.update({
        k[6:].lower(): v
        for k, v in os.environ.items()
        if k.startswith('INPUT_')
        and k[6:].lower() not in inputs
        and not any(s in k for s in [
            'API_KEY',
            'EVENT',
            'TOKEN'
        ])
    })

    # Convert inputs to list format for argparse
    args_list = []
    for k, v in inputs.items():
        if k == 'opts':
            args_list.extend(v.split())
        elif k == 'slugs':
            args_list.extend(['--slugs', ','.join(v.split())])
        elif k == 'sort':
            args_list.extend(['--color-sort', v])
        elif k == 'style':
            args_list.extend(['--badge-style', v])
        elif k == 'verify' or k == 'reverse':
            if v.lower() == 'true':
                args_list.append(f'--{k}')
        else:
            args_list.extend([f'--{k}', v])

    logger.debug(args_list)

    main(args_list)
