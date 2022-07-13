from main import parser

raw_txt = """[2022-05-25T06:38:13.956Z] "GET / HTTP/1.1" 200 - via_upstream - "-" 0 35430 6 6 "-" "Python/3.9 aiohttp/3.8.1" "e4c5583b-565c-9026-8e5d-974bdf8ab467" "service2.prod:4000" "10.42.2.204:4000" inbound|4000|| 127.0.0.6:56089 10.42.2.204:4000 10.42.3.252:54568 - default "GET /" service2(200)|"""
# raw_txt = """[2022-05-25T06:38:13.956Z] "GET / HTTP/1.1" 200 - via_upstream - "-" 0 35430 6 6 "-" "Python/3.9 aiohttp/3.8.1" "e4c5583b-565c-9026-8e5d-974bdf8ab467" "service2.prod:4000" "10.42.2.204:4000" inbound|4000|| 127.0.0.6:56089 10.42.2.204:4000 10.42.3.252:54568 - default "GET /" service2(200)|service3(200)|"""

print(raw_txt)

result = parser(raw_txt)

import json
print(json.dumps(result, indent=2))
