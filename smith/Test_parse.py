import requests
import urllib.parse
from bs4 import BeautifulSoup
from smith.wiki_doc_pair_pb2 import WikiDoc, Section, WikiDocPair
import tensorflow as tf

def  Read_doc(doc_url):
    # 1. Read the URL
    url = urllib.parse.quote(doc_url, safe=':/?&=')
    response = requests.get(url)
    html_content = response.text

    # 2. Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")


    # Extract relevant information from the HTML structure using BeautifulSoup
    title = soup.title.string.strip().replace("- Wikipedia","")

    document=soup.find("div",class_="mw-body-content")
    description=""
    i=0

    while(len(description)<1):
        description = document.find_all("p")[i].text.strip()
        i=i+1
    sections = []

    # Assume you have a way to identify and loop through sections in the HTML
    if(document):
        for section_element in document.find_all(["h2", "h3", "h4", "h5", "h6"]):
            section_title = section_element.text.strip().replace("[edit]","")

            # Find the next sibling until the next section or the end of the document
            section_text = ""
            sibling = section_element.find_next_sibling()
            while sibling and sibling.name not in ["h2", "h3", "h4", "h5", "h6"]:
                section_text += str(sibling).replace("\n", "").replace("\t", "")
                sibling = sibling.find_next_sibling()

            section_text = BeautifulSoup(section_text, "html.parser").text.strip()

            section = Section(title=section_title, text=section_text)
            sections.append(section)

        # 3. Create Protobuf Objects
    return WikiDoc(url=url,title=title, description=description, section_contents=sections)

wiki_data=[]
with open("smith/data/data/gwikimatch_v2_human_neg_1.test_external_wdp.filtered_contro_wiki_cc_team.only_urls.tsv", 'r', encoding='utf-8') as file:
    # Read each line in the file
    for line in file:
        # Process each line (you can replace this with your own logic)
        wiki_data.append(line.strip().split("\t"))

wiki_pairs=[]
with tf.io.TFRecordWriter("test.tfrecord") as writer:
    for i in range(0,200):
        # print(i)
        wiki_pair=WikiDocPair(human_label_for_classification=int(wiki_data[i][0]),doc_one=Read_doc(wiki_data[i][1]),doc_two=Read_doc(wiki_data[i][2]))
        # print(wiki_pair)
        # break
        
        writer.write(wiki_pair.SerializeToString())
    #wiki_pairs.append(wiki_pair)
# print(serialized_data))
# wiki_pair=WikiDocPair(human_label_for_classification=int(wiki_data[0][0]),doc_one=Read_doc(wiki_data[0][1]),doc_two=Read_doc(wiki_data[0][2]))
# print(Read_doc(wiki_data[0][2]))
# 4. Serialize and use the Protobuf Object
#serialized_data = wiki_pairs.SerializeToString()
# print(serialized_data)

# with tf.io.TFRecordWriter("example.tfrecord") as writer:
#     writer.write(serialized_data)