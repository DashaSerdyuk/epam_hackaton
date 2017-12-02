import pandas as pd


def process_engine(lat, lon):
    return "Hey, your NEW location is (00{0};11{1}).".format(lat, lon), '', (lat, lon)