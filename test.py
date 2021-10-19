import unittest
from Xtern import get_info, interactive_visualizations, top_ten, Event, add_info
import googlemaps
import pandas as pd
import time
import plotly.express as px
from eventbrite import Eventbrite
from predicthq import Client
import requests
import json
import reverse_geocoder as rg
import shutil
from os.path import exists

class TestFileName(unittest.TestCase):
    def test_functions(self):
        df = pd.DataFrame(pd.read_excel("Data.xlsx"))
        new_df = pd.DataFrame(pd.read_excel("Output.xlsx"))
        a = get_info(df["Address"][1],15,"restaurant")
        b = interactive_visualizations(new_df)
        c = top_ten(a,200)
        d = Event(df["Address"][1])
        e = add_info(df["Address"][1])
        self.assertTrue(type(a) is pd.core.frame.DataFrame)
        self.assertTrue(type(b) is str)
        self.assertTrue(type(c) is pd.core.frame.DataFrame)
        self.assertTrue(type(d) is list)

if __name__ == '__main__':
    unittest.main()
