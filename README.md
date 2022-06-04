# Translate .po files with Google Translate

Why doesn't this exist? I have no idea - if you have a google cloud account, it's super easy to do.

1. Set up a google cloud account. I recommend a [service account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account). and [here](https://cloud.google.com/translate/docs/setup) is a good place to start.
2. install polib and google translate libraries for python.

```bash
pip install polib
pip install google-cloud-translate
```

3. use the script to translate the .po files.

```bash
python translate.py /path/to/input.po /path/to/output.po
```

enjoy
