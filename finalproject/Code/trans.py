#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""Simple command-line example for Translate.
Command-line application that translates some text.
"""
from __future__ import print_function

from googleapiclient.discovery import build


def main():

  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build('translate', 'v2',
            developerKey='AIzaSyAX3xkncThOgOZYNGwnI16_sfgK02HQYA4')
  print(service.translations().list(
      source='en',
      target='fr',
      q=['flower', 'car']
    ).execute())

if __name__ == '__main__':
  main()