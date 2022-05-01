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

print(client.collections['news'].documents.search({
    'q': 'auckland home',
    'query_by': 'headline, summary, keywords',
}))


# drop_response = client.collections['news'].delete()
# print(drop_response)