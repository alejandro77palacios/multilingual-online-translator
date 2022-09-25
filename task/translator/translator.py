import sys
import requests
from bs4 import BeautifulSoup

languages = {1: "Arabic",
             2: "German",
             3: "English",
             4: "Spanish",
             5: "French",
             6: "Hebrew",
             7: "Japanese",
             8: "Dutch",
             9: "Polish",
             10: "Portuguese",
             11: "Romanian",
             12: "Russian",
             13: "Turkish"}

directions = ("french-english", "english-french")
url = "https://context.reverso.net/translation"


def translate(word, origin, dest):
    url_translate = url + "/" + origin.lower() + "-" + dest.lower() + "/" + word
    try:
        response = requests.get(url_translate, headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    else:
        return response


def get_translations(soup):
    find_translations = soup.find_all("span", class_="display-term")
    list_translations = [trans.text.strip() for trans in find_translations]
    return list_translations


def get_examples(soup):
    examples = []
    div_tags = soup.find("section", {"id": "examples-content"}).find_all("div", {"class": "example"})
    for div_tag in div_tags:
        span_tags = div_tag.find_all("span", {"class": "text"})
        for span_tag in span_tags:
            examples.append(span_tag.text.strip())
    return examples


def process_translation(word, origin, dest):
    r = translate(word, origin, dest)
    soup = BeautifulSoup(r.content, 'html.parser')
    translations = get_translations(soup)
    examples = get_examples(soup)
    dict_process = {'translations': translations, 'examples': examples}
    if len(dict_process['translations']) == 0 or len(dict_process['examples']) == 0:
        print(f'Sorry, unable to find {word}')
        sys.exit()
    return dict_process


def show_translations(dest_language, translations):
    print()
    print(dest_language, "Translations:")
    print(*translations[:5], sep="\n", end="")


def show_examples(dest_language, examples):
    print()
    print(dest_language, "Examples:")
    for i in range(5):
        print(examples[i] + '\n')


def translate_all(word, origin):
    dict_translations = {}
    for i in languages:
        dest = languages[i]
        if dest.lower() == origin:
            continue
        else:
            dict_translations[dest] = process_translation(word, origin, dest)
    return dict_translations


def write_translations(word, origin):
    dict_translations = translate_all(word, origin)
    with open(word + '.txt', 'w') as f:
        for dest in dict_translations:
            f.write(dest + " Translations:\n")
            f.write(dict_translations[dest]['translations'][0] + '\n\n')
            f.write(dest + " Example:\n")
            f.write(dict_translations[dest]['examples'][0] + '\n')
            f.write(dict_translations[dest]['examples'][1] + '\n\n\n')


def main():
    args = sys.argv
    # args = [0, 'english', 'korean', 'hello']
    origin = args[1]
    dest = args[2]
    word = args[3]
    if dest == 'all':
        write_translations(word, origin)
    elif dest.capitalize() not in languages.values():
        print(f"Sorry, the program doesn't support {dest}")
        sys.exit()
    else:
        my_translations = process_translation(word, origin, dest)
        with open(word + '.txt', 'w') as f:
            f.write(dest + " Translations:\n")
            f.write(my_translations['translations'][0] + '\n\n')
            f.write(dest + " Example:\n")
            f.write(my_translations['examples'][0] + '\n')
            f.write(my_translations['examples'][1] + '\n\n\n')
    with open(word + '.txt') as f:
        print(f.read())


main()
