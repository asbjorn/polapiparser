# -*- coding: utf-8 -*-
"""Vinmonopolet's parser

Usage:
  read.py search <name>
  read.py get <type> 
  read.py (-h | --help)
  read.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import requests
import itertools
import functools
from docopt import docopt

API_URL = 'http://www.vinmonopolet.no/api/produkter'


def to_int(value):
    if value is not None and value != '':
        return int(value)
    return None


def to_float(value):
    if value == 'Ukjent':
        return None
    if value is not None and value != '':
        return float(value.replace(',', '.'))
    return None


def parse_line(line):
    columns = line.split(';')
    return {
        'Datotid': columns[0],
        'Varenummer': columns[1],
        'Varenavn': columns[2],
        'Volum': to_float(columns[3]),
        'Pris': to_float(columns[4]),
        'Literpris': to_float(columns[5]),
        'Varetype': columns[6],
        'Produktutvalg': columns[7],
        'Butikkategori': columns[8],
        'Fylde': to_int(columns[9]),
        'Friskhet': to_int(columns[10]),
        'Garvestoffer': to_int(columns[11]),
        'Bitterhet': to_int(columns[12]),
        'Sodme': to_int(columns[13]),
        'Farge': columns[14],
        'Lukt': columns[15],
        'Smak': columns[16],
        'Passertil': [columns[17], columns[18], columns[19]],
        'Land': columns[20],
        'Distrikt': columns[21],
        'Underdistrikt': columns[22],
        'Argang': to_int(columns[23]),
        'Rastoff': columns[24],
        'Metode': columns[25],
        'Alkohol': to_float(columns[26]),
        'Sukker': to_float(columns[27]),
        'Syre': to_float(columns[28]),
        'Lagringsgrad': columns[29],
        'Produsent': columns[30],
        'Grossist': columns[31],
        'Distributor': columns[32],
        'Emballasjetype': columns[33],
        'Korktype': columns[34],
        'Vareurl': columns[35],
    }


def read_data():
    d = requests.get(API_URL)
    d.encoding = 'ISO-8859-1'
    return (parse_line(line.encode('utf-8'))
            for line in d.text.splitlines()[1:])


def get_all_beers(data):
    """Returns a generator with a filter on 'Varetype' = u'Øl'
    """
    return itertools.ifilter(lambda x: is_type(u'Øl', x), data)


def get_types(data):
    return set((t['Varetype'] for t in data))


def is_type(type, product):
    """Return true if the item is of the type requested.

    >>> is_type(u'Øl', {'Varetype': u'Øl'}) == True
    >>> is_type(u'Vin', {'Varetype': u'Øl'}) == False
    """
    return product['Varetype'] == type.encode("utf-8")


def search(name, all_beers):
    """Return all matching beer dicts within the 'all_beers'
    collection of beers.
    """
    return [b for b in all_beers
            if name.lower() in b.get('Varenavn').lower()]


if __name__ == '__main__':
    arguments = docopt(__doc__, version="Vinmonopolet 0.1")

    data = read_data()
    is_beer = functools.partial(is_type, u'Øl')
    all_beers = get_all_beers(data)

    if 'search' in arguments:
        found_beers = search(arguments['<name>'], all_beers)
        if found_beers:
            for beer in found_beers:
                print("Name: {Varenavn}\n"
                      "  Country: {Land}\n"
                      "  Alcohol: {Alkohol}\n"
                      "  Price: {Pris} NOK\n".format(**beer))
        else:
            print("No beer with the name: '{}'".format(arguments['<name>']))

    elif 'get' in arguments:
        raise NotImplementedError("Will come soon")
