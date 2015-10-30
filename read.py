# -*- coding: utf-8 -*-
import requests
import itertools
import functools

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
    return (parse_line(line) for line in d.text.splitlines()[1:])


def get_types(data):
    return set((t['Varetype'] for t in data))


def is_type(type, product):
    return product['Varetype'] == type


if __name__ == '__main__':
    data = read_data()

    is_beer = functools.partial(is_type, u'Øl')
    all_beers = itertools.ifilter(is_beer, data)
    for beer in all_beers:
        print("{} - {}".format(
            beer.get('Produsent').encode("utf-8"),
            beer.get('Varenavn').encode("utf-8")))

    all_types = get_types(data)
    for t in all_types:
        print("Type: {}".format(t.encode("utf-8")))
