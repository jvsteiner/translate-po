#!/usr/bin/env python3
import six
from google.cloud import translate_v2 as translate
import polib


def translate_text(text, target='lv', source='en'):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target, source_language=source)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result['translatedText']


def main(args):
    pofile = polib.pofile(args[0])
    for entry in pofile:
        entry.msgstr = translate_text(entry.msgid)
    pofile.save(args[1])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
