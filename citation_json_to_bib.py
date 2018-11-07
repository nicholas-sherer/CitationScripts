# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 12:42:49 2018

@author: nashere2

File for turning json citation data from pubmed URLs into bibtex citations
"""

import json
import urllib


def get_dict(link):
    '''Fetch the json data for a citation from a PMC link and load into a
    python dictionary.'''
    f = urllib.request.urlopen(link)
    citation_json = f.read()
    citation_dict = json.loads(citation_json)
    return citation_dict


def kv_to_string(sample_dict, key):
    '''Output the latex for one entry in a python dictionary'''
    return key.lower() + ' = {' + sample_dict[key] + '},\n'


def json_authors_to_latex(sample_dict):
    '''Convert author list into latex format.'''
    author_list = sample_dict['author']
    head = author_list[0]
    tail = author_list[1:]
    author_str = head['family'] + ', ' + head['given']
    for author in tail:
        author_str = author_str + ' and ' + author['family'] + \
            ', ' + author['given']
    return 'author = {' + author_str + '},\n'


def json_title_to_latex(sample_dict):
    '''Convert title into latex format.'''
    return kv_to_string(sample_dict, 'title')


def json_journal_to_latex(sample_dict):
    '''Convert journal into latex format.'''
    return 'journal = {' + sample_dict['container-title'] + '},\n'


def json_publisher_to_latex(sample_dict):
    '''Convert publisher into latex format.'''
    return kv_to_string(sample_dict, 'publisher')


def json_volume_to_latex(sample_dict):
    '''Convert volume into latex format.'''
    return kv_to_string(sample_dict, 'volume')


def json_number_to_latex(sample_dict):
    '''Convert issue/number into latex format.'''
    return 'number = {' + sample_dict['issue'] + '},\n'


def json_pages_to_latex(sample_dict):
    '''Convert pages into latex format.'''
    return 'pages = {' + sample_dict['page'] + '},\n'


def json_year_to_latex(sample_dict):
    '''Convert year into latex format.'''
    return 'year = {' + str(sample_dict['issued']['date-parts'][0][0]) + '},\n'


def json_issn_to_latex(sample_dict):
    '''Convert issn into latex format.'''
    return kv_to_string(sample_dict, 'ISSN')


def json_to_latex_label(sample_dict):
    '''Makes a LaTeX label of the first author's last name then the year then
    'a'.'''
    first_author = sample_dict['author'][0]
    last_name = first_author['family']
    year = str(sample_dict['issued']['date-parts'][0][0])
    return last_name + year + 'a'


conversions = [json_authors_to_latex, json_title_to_latex,
               json_journal_to_latex, json_publisher_to_latex,
               json_volume_to_latex, json_number_to_latex,
               json_pages_to_latex, json_year_to_latex,
               json_issn_to_latex]


def json_full_to_latex(sample_dict):
    '''Convert python dict of json citation data to bibtex formatted entry.'''
    final_str = '@article{' + json_to_latex_label(sample_dict) + ',\n'
    for func in conversions:
        try:
            final_str = final_str + '\t' + func(sample_dict)
        except KeyError:
            pass
    final_str = final_str + '}\n'
    return final_str


def make_bibtex_from_urls(url_file, bibtex_file_name):
    '''Convert a file of urls with json citation data into a bibtex formatted
    entry.'''
    url_list = open(url_file).readlines()
    with open(bibtex_file_name, 'w', encoding='UTF-8') as bibtex_file:
        for url in url_list:
            json_dict = get_dict(url)
            bibtex_entry = json_full_to_latex(json_dict)
            bibtex_file.write(bibtex_entry + '\n')


if __name__ == '__main__':
        import sys
        from datetime import datetime
        if len(sys.argv) >= 3:
            file_name = sys.argv[2]
        else:
            file_name = 'bibtex' + str(datetime.utcnow())
        make_bibtex_from_urls(sys.argv[1], file_name)
