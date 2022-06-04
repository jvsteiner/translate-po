#!/usr/bin/env python3
import argparse
import six
from google.cloud import translate_v2 as translate
import polib
import asyncio
from concurrent.futures import ThreadPoolExecutor


def count_spaces(s):
    left = len(s) - len(s.lstrip())
    right = len(s) - len(s.rstrip())
    return (left*" ", right*" ")


def replace_spaces(s, counts):
    return counts[0] + s + counts[1]


def translate_text(text, args):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    whitespace = count_spaces(text)
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=args.target, source_language=args.source)

    return replace_spaces(result['translatedText'], whitespace)


async def in_thread(func, text, args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, func, text, args)


async def main(args):
    pofile = polib.pofile(args.input[0])

    results = await asyncio.gather(
        *(in_thread(translate_text, pofile[i].msgid, args) for i in range(len(pofile))))

    for i in range(len(results)):
        pofile[i].msgstr = results[i]

    pofile.save(args.output[0])


if __name__ == '__main__':
    global _executor
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='I', type=str, nargs=1,
                        help='the input file')
    parser.add_argument('output', metavar='O', type=str, nargs=1,
                        help='the output file')
    parser.add_argument(
        '--threads', help='Number of requests to make concurrently (default 20)', type=int, default=20)
    parser.add_argument(
        '--source', help='The source language in the pofile (default en)', type=str, default='en')
    parser.add_argument(
        '--target', help='The target language for the pofile (default lv)', type=str, default='lv')
    args = parser.parse_args()
    _executor = ThreadPoolExecutor(args.threads)
    asyncio.run(main(args))
