#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--layout", help="layout file")
parser.add_argument("-e", "--entries", help="entries")
parser.add_argument("-f", "--file", help="file containing the entries")
parser.add_argument("-d", "--datatype", help="data type, json plain_newlines or plain_commas (default)")
parser.add_argument("-p", "--position", help="x and y of the window")
parser.add_argument("-t", "--theme", help="change gtk theme, specifying a gtkrc file path")

args = parser.parse_args()


def get():
	global args
	return args
