__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.nerd import html_generate


def extract_name(word_list):
    """ (list) --> (list)
        extracts the words in a list that can refer to name
    """
    name_indexes = []
    for index, word in enumerate(word_list):
        if word[0].isupper() and index > 0 and len(word) > 1:
            name_indexes.append(index)
    return name_indexes


def main():
    log('importing names')
    the_query = "SELECT name, type FROM meertens_names"
    cur = basic.run_query(None, the_query)
    name_dict = {}
    name_list = []
    for c in cur.fetchall():
        name_dict[c[0].lower()] = c[1]
        name_list.append(c[0].lower())

    log('importing notarial acts')
    the_query = "SELECT inhoud1, inhoud2, inhoud3, datering, plaats from notary_acts"
    cur = basic.run_query(None, the_query)
    notarial_list = []
    for c in cur.fetchall()[:1000]:
        # each notarial_list element is [text, date, place]
        notarial_list.append([c[0] + ' ' + c[1] + ' ' + c[2], c[3], c[4]])

    log('extracting names')
    output = []
    for n in notarial_list:
        text = n[0]
        index_dict = {}
        text = basic.text_pre_processing(text)
        for index, word in enumerate(text.split()):
            # uses Meertens data
            if not word == 'van' and name_dict.get(word.lower()):
                index_dict[index] = name_dict.get(word.lower())

            # uses the first uppercase character
            # if word[0].isupper() and index > 0 and len(text.split()[index-1]) > 1:
            #     index_dict[index] = "last_name"
            # else:
            #     if word[0].isupper() and index > 0:
            #         index_dict[index] = "first_name_m"

        output.append([text, index_dict])

    html_generate.export_html(output)

if __name__ == "__main__":
    main()