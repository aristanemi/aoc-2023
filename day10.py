#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import re

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]

