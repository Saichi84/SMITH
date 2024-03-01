# import tensorflow as tf
# from google.protobuf.json_format import MessageToJson
# for example in tf.python_io.tf_record_iterator("data/small_demo_data.external_wdp.filtered_contro_wiki_cc_team.tfrecord"):
#     #print(tf.train.Example.FromString(example))
#     jsonMessage = MessageToJson(tf.train.Example.FromString(example))
#     print(jsonMessage)
import collections
import random

import nltk
import tensorflow.compat.v1 as tf
import tqdm

import requests
import urllib.parse
from bs4 import BeautifulSoup

from smith import utils
from smith import wiki_doc_pair_pb2
from smith.bert import tokenization

import tensorflow as tf 
# raw_dataset = tf.io.TFRecordWriter("data/small_demo_data.external_wdp.filtered_contro_wiki_cc_team.tfrecord")
# #raw_dataset=raw_dataset.map(map_fn)
# print((raw_dataset))
# # for raw_record in raw_dataset:
# #     #example = tf.train.Example()
# #     #example.ParseFromString(raw_record.numpy())
# #     print(raw_record)


# wiki_doc_pair = wiki_doc_pair_pb2.WikiDocPair()
# instances = []
# # Add some counters to track some data statistics.
# i=0
# sent_token_counter = [0, 0]
# for example in tqdm.tqdm(tf.python_io.tf_record_iterator("example.tfrecord")):
#     doc_pair = wiki_doc_pair.FromString(example)
#     i=i+1
#     if(i==1):
#         print(doc_pair)
#         break

url = urllib.parse.quote("https://en.wikipedia.org/wiki/Caitlin_Farrell#Professional_career", safe=':/?&=')
response = requests.get(url)
html_content = response.text

# 2. Parse HTML
soup = BeautifulSoup(html_content, "html.parser")


# Extract relevant information from the HTML structure using BeautifulSoup
title = soup.title.string.strip().replace("- Wikipedia","")
print(title)
