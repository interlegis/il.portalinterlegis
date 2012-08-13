# -*- coding: utf-8 -*-
from manager import get_template

def colab(context):
    return get_template('colab.html').render()
