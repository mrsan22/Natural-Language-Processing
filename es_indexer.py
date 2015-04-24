__author__ = 'sanjiv'

from pyelasticsearch import ElasticSearch
def es_indexer():
    es=ElasticSearch('http://localhost:9200/')
    if es:
        # Delete index /sentiment_analysis if it already exists
        try:
            es.delete_index("sentiment_analysis")
            print "Deleted index sentiment_analysis if it already existed."
        except:
            raise 'ElasticHttpNotFoundError'
        finally:
            print "Creating index sentiment_analysis ...."
            es.create_index("sentiment_analysis",{
                                    'settings': {
                                        'index': {
                                            'store': {
                                                'type': "default"
                                            },
                                            'number_of_shards': 1,
                                            'number_of_replicas': 1
                                        },
                                        'analysis': {
                                            'analyzer': {
                                                'default_english': {
                                                    'type': 'english'
                                                }
                                            }
                                        }
                                    },
                                    "mappings": {
                                        "document": {
                                            "properties": {
                                                "text": {
                                                    "type": "string",
                                                    "store": True,
                                                    "index": "analyzed",
                                                    "term_vector": "with_positions_offsets_payloads",
                                                    "analyzer": "default_english"
                                                },
                                                "sentiment": {
                                                    "type": "string",
                                                    "store": True,
                                                    "index": "analyzed",
                                                    "analyzer": "default_english"
                                                }
                                            }
                                        }
                                    }
                                })
            print "Created index 'sentiment_analysis' with type 'document' and an analyzed field 'text'."
    else:
        print "ElasticSearch is not running or the default cluster is down."
