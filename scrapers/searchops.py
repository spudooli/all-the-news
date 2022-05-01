import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': 'aOY37YzmNajlFtblSeCJL87w9DYBbEiBHNhzpqpontc2Ile2',
  'connection_timeout_seconds': 2
})

news_schema = {
  'name': 'news',
  'fields': [
    {'name': 'id', 'type': 'string' },
    {'name': 'headline', 'type': 'string' },
    {'name': 'summary', 'type': 'string' },
    {'name': 'datetime', 'type': 'int64' },
    {'name': 'source', 'type': 'string', 'index': False, "optional": True },
    {'name': 'keywords', 'type': 'string' },
    {'name': 'url', 'type': 'string', 'index': False, "optional": True }
  ]
}

client.collections.create(news_schema)

