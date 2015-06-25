# -*- coding: utf-8 -*-
from __future__ import unicode_literals

letters = {
    'А': '.-',
    'Б': '-...',
    'В': '.--',
    'Г': '--.',
    'Д': '-..',
    'Е': '.',
    'Ж': '...-',
    'З': '--..',
    'И': '..',
    'Й': '.---',
    'К': '-.-',
    'Л': '.-..',
    'М': '--',
    'Н': '-.',
    'О': '---',
    'П': '.--.',
    'Р': '.-.',
    'С': '...',
    'Т': '-',
    'У': '..-',
    'Ф': '..-.',
    'Х': '....',
    'Ц': '-.-.',
    'Ч': '---.',
    'Ш': '----',
    'Щ': '--.-',
    'Ъ': '--.--',
    'Ы': '-.--',
    'Ь': '-..-',
    'Э': '..-..',
    'Ю': '..--',
    'Я': '.-.-',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '.': '......',
    ',': '.-.-.-',
    ':': '---...',
    ';': '-.-.-.',
    '(': '-.--.-',
    '`': '.----.',
    '"': '.-..-.',
    '-': '-....-',
    '?': '..--..',
    '!': '--..--',
    'z': '-...-',
}

reverse_letters = dict(zip(letters.values(), letters.keys()))


def translate_word(code):
    chars = filter(None, code.split('б'))

    result = ''

    for char in chars:
        code = ''.join(map(lambda c: '.' if c.islower() else '-', char))
        if code in reverse_letters:
            result += reverse_letters[code]
        else:
            raise ValueError()

    return result


def translate(string):
    words = filter(None, string.split('бб'))

    result = []

    if string[0] == 'б':
        result.append('')

    for word in words:
        result.append(translate_word(word))

    if string[-1] == 'б':
        result.append('')

    return ' '.join(result)
