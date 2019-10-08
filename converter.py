# -*- coding: utf-8 -*-
# File: cnki-converter/converter.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-10-07 17:13:28
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from random import choices
from os.path import split, join, exists

month_abbr = [
    '', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
    'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]


def rand_code():
    """return random code"""
    return ''.join(choices(list('abcdefghijkl'), k=5))


def reader(filepath):
    """ref file reader: return list of {key: value}"""
    dynamic_item = {}
    with open(filepath, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('%'):
                temp = line.split(' ')
                k, v = temp[0], (' '.join(temp[1:])).strip()
                if v != 'CNKI':
                    if k == '%A':
                        dynamic_item.setdefault('%A', [])
                        dynamic_item['%A'].append(v)
                    else:
                        dynamic_item[k] = v
                else:
                    yield dynamic_item
                    dynamic_item = {}


def adapter(adp_name):
    """ref adapters"""
    def to_pages(p):
        sp, ep = p.split('-')
        return sp, ep

    def to_entry(item):
        result = ""
        for k, v in item.items():
            if k == 'A1':
                for author in v:
                    result += '{} - {}\n'.format(k, author)
            else:
                result += '{} - {}\n'.format(k, v)
        result += '\n\n\n'
        return result

    def endnote(item):
        mapping = {
            '%0': 'TY',  # type ok
            '%A': 'A1',  # 1st author ok
            '%X': 'AB',  # abstract
            # '%K': 'KW',  # keywords
            # '%+': '',  # 机构
            '%T': 'T1',  # title ok
            '%D': 'Y1',  # year ok
            # '%N': 'IS',  # Issue or Month ok
            '%J': 'JO',  # Journal name ok
            '%P': '',  # Pages #TODO
            '%V': 'VL',  # volume
            # 'ER': '',  # end of ref must be empty.
        }
        type_mapping = {
            'Journal': 'JOUR',
            'Conference': 'CONF',
            'Thesis': 'THES',
            'Book': 'BOOK'
        }
        temp = {}
        for k, v in mapping.items():
            value = item.get(k)
            if value:
                if k == '%P':
                    temp['SP'], temp['EP'] = to_pages(value)
                elif k == '%0':
                    temp[v] = type_mapping[value.split(' ')[0]]
                elif k == '%N':
                    temp[v] = month_abbr[int(value)]
                else:
                    temp[v] = value

                if temp['TY'] == 'THES':
                    temp['PB'] = item.get('%I')
                    temp['JO'] = item.get('%I')
        temp['ER'] = ''

        return to_entry(temp)

    return {'endnote': endnote}[adp_name]


def dump(orig_file_name, lines):
    head, tail = split(orig_file_name)
    fp = None
    while True:
        tail = tail.split('.')[0] + '_{}.ris'.format(rand_code())
        fp = join(head, tail)
        if not exists(fp):
            break
    with open(join(head, tail), 'w+', encoding='utf-8') as f:
        f.writelines(lines)
    return fp


def converter(filepath):
    """converter"""
    all_lines = ""
    item_count = 0
    for item in reader(filepath):
        ris_entry = adapter('endnote')(item)
        print(ris_entry)
        all_lines += ris_entry
        item_count += 1
    assert len(all_lines) > 3
    return dump(filepath, all_lines), item_count


if __name__ == "__main__":
    converter(
        '/Users/mingshicai/Documents/workspace/python/qt/cnki-converter/demo.txt')
