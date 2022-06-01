#-*- coding: utf-8 -*-
from src.kernel import Server
from config import settings

if(__name__ == '__main__'):
    Server(*settings).launch()
