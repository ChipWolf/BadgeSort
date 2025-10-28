#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import io
from contextlib import redirect_stdout

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
        elif v and k == 'slugs':
            args_list.extend(['--slugs', ','.join(v.split())])
        elif v and k == 'sort':
            args_list.extend(['--color-sort', v])
        elif v and k == 'style':
            args_list.extend(['--badge-style', v])
        elif v and k in ['verify', 'reverse', 'embed-svg', 'skip-logo-check']:
            if v.lower() == 'true':
                args_list.append(f'--{k}')
        elif v and k == 'thanks':
            if v.lower() == 'false':
                args_list.append('--no-thanks')
        else:
            if v:
                args_list.extend([f'--{k}', v])

    logger.debug(args_list)

    # Capture stdout from icons.main so we can emit it to GITHUB_OUTPUT
    buf = io.StringIO()
    exit_code = 0
    try:
        with redirect_stdout(buf):
            main(args_list)
    except SystemExit as e:
        # Preserve exit code from the underlying CLI
        try:
            exit_code = int(e.code) if e.code is not None else 0
        except Exception:
            exit_code = 1
    except Exception:
        # Unexpected error
        exit_code = 1

    output_text = buf.getvalue().strip()

    # If we produced stdout (i.e., no --output file was used), expose it as a step output
    github_output_path = os.environ.get('GITHUB_OUTPUT')
    if output_text and github_output_path:
        delimiter = 'BADGESORT_EOF'
        try:
            with open(github_output_path, 'a', encoding='utf-8') as fh:
                fh.write(f"badges<<{delimiter}\n")
                fh.write(output_text)
                if not output_text.endswith("\n"):
                    fh.write("\n")
                fh.write(f"{delimiter}\n")
            logger.debug('Wrote badges output to GITHUB_OUTPUT.')
        except Exception as e:
            logger.error(f"Failed to write to GITHUB_OUTPUT: {e}")

    sys.exit(exit_code)
