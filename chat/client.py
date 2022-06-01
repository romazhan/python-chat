#-*- coding: utf-8 -*-
from src.kernel import Client
from config import settings

if(__name__ == '__main__'):
    Client().connect(*settings)
