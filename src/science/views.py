# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import RequestContext


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


letters = {
    'A': '.-',
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


def translate(string):
    chars = filter(None, string.split('р'))

    result = ''

    for char in chars:
        code = ''.join(map(lambda c: '.' if c.islower() else '-', char))
        if code in reverse_letters:
            result += reverse_letters[code]
        else:
            return ''

    return result


def index(request):
    translate('')
    context = {
        'a': request.POST.get('a', ''),
        'b': request.POST.get('b', ''),
        'message': '',
        'check': request.POST.get('check', request.GET.get('check', '')),
    }

    if request.POST:
        if context['a'] and context['b']:
            a = translate(context['a'])
            b = translate(context['b'])

            if a and b:
                if len(a) == len(b):
                    context['message'] = 'Есть совпадение'
                else:
                    context['message'] = 'Нет совпадения'

                if context['check']:
                    context['message'] += '|a:' + a + '|b:' + b + '|'

            elif not a:
                context['message'] = 'Строка А не распознается.'

            elif not b:
                context['message'] = 'Строка B не распознается.'

        else:
            context['message'] = 'Введите две строки для сравнения'

    return render_to_response(request, 'science/index.html', context)
