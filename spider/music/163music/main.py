import requests
headers = {
    'Referer':
    'google.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
}
s = requests.get(
    'http://219.153.49.228:43528/x_search_index.php', headers=headers)
print(s.text)