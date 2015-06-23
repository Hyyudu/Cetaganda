# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from science.utils import translate


def test_translate():
    assert translate('нН') == 'A'
    assert translate('бнНб') == ' A '
    assert translate('ннбНнНн') == 'ИЦ'
    assert translate('нНббнН') == 'A A'
