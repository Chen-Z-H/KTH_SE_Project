import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


# def search(url, term):
#     return 0

# r = requests.get('http://localhost:9200')
client = Elasticsearch()

def query_low_level(query_json):
    with open(query_json, 'r') as f:
        query1 = json.load(f)

    # client = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    response = client.search(index="simple", body=query1)

    for hit in response["hits"]["hits"]:
        print(hit["_id"], ": ", hit["_score"])

def query_high_level(query_json):
    with open(query_json, 'r') as f:
        query1 = json.load(f)

def query_dsl(keywords):
    # s = Search(using=client, index="_articles").query("match", )
    s = Search(using=client, index="simple") \
        .query("match", types="bar") \
        .query("match", types="establishment") \
        .exclude("match", types="restaurant")

    response = s.execute()

    for hit in response:
        print(hit.meta.id, ": ", hit.meta.score)


def query(keywords):
    # s = Search(using=client, index="_articles").query("match", )
    # s = Search(using=client, index="articles") \
    #     .query("match", title=keywords) \
    #     .query("match", text=keywords) \
    #     .exclude("match", text="REDIRECT")

    # Query all the data
    s = Search(using=client, index="articles") \
        .query("match_all") \
        # .exclude("match", text="REDIRECT")

    # s.aggs.bucket('category', 'terms', field='categories')

    response = s.execute()

    print(response.took)
    for hit in response:
        print("ID: ", hit.meta.id, ", Title: ", hit.title,
              ", Score: ", hit.meta.score, ", Category: ", hit.categories)

    json_response = json.dumps(response.to_dict(), indent=1)
    print(json_response)


# query_low_level('query1.json')
query("China")

# data = {
#     'no': 1,
#     'name': 'zehua',
#     'url:': 'www.google.com'
# }
#
# # Turn the python data to json type
# json_str = json.dumps(data, indent=1)
#
# print("Original data: ", repr(data))
# print("Json: ", json_str)
#
# # Turn the json into python dictionary type
# data2 = json.loads(json_str)
# print("Recovered data: ", data2)
#
#
# # Write json data to file
# with open('data.json', 'w') as f:
#     json.dump(data, f)
#
# # Load json data from file
# with open('data.json', 'r') as f:
#     data = json.load(f)

