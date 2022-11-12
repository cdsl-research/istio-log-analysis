import pathlib
import re
import argparse
import json


match_pattern = (
    # '[2022-05-12T00:57:09.548Z]'
    r"\[(?P<DateTime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)]"
    r' "(?P<Method>[^ ]+)'  # 'GET'
    r" (?P<Path>[^ ]+)"  # '/author'
    r' (?P<Protocol>[^ ]+)"'  # 'HTTP/1.1'
    r" (?P<Status>\d{,3})"  # '200'
    r' (?P<ResponseFlags>[^ ]+)'  # '-'
    r' (?P<ResponseCodeDetails>[^ ]+)'  # 'via_upstream'
    r' (?P<ConnectionTerminationDetails>[^ ]+)'  # '-'
    r' "(?P<UpstreamTransportFailureReason>[^"]+)"'  # '"-"'
    r" (?P<BytesReceived>[-\d]+)"  # '0 11462 7 7'
    r" (?P<BytesSent>[-\d]+)"  # '0 11462 7 7'
    r" (?P<Duration>[-\d]+)"  # '0 11462 7 7'
    r" (?P<RespXEnvoyUpstreamServiceTime>[-\d]+)"  # '0 11462 7 7'
    r' "(?P<XForwardFor>[\.,\-\w]+)"'  # "192.168.200.1,10.42.0.0"
    r' "(?P<UserAgent>[^"]+)"'  # "Python/3.9 aiohttp/3.8.1"
    r' "(?P<ReqId>[\-\w]+)"'  # '"ef217580-7229-9d84-b9b2-8d7bd3dfcca4"'
    r' "(?P<ReqAuthority>[\-\:\.\w]+)"'  # '"paper-app.paper:4000"'
    r' "(?P<UpstreamHost>[\-\:\.\d]+)"'  # '"10.42.3.158:8000"'
    # 'outbound|4000||paper-app.paper.svc.cluster.local'
    r" (?P<UpstreamCluster>\w+\|\d+\|\w*\|[\-\.\w]*)"
    r" (?P<UpstreamLocalAddr>[\-\:\.\w]+)"  # '10.42.3.121:58312'
    r" (?P<DownstreamLocalAddr>[\:\.\w-]+)"  # '10.43.148.153:9200'
    r" (?P<DownstreamRemoteAddr>[\:\.\w-]+)"  # '10.42.3.163:47890'
    # 'outbound_.8000_._.httpbin.foo.svc.cluster.local'
    r" (?P<ReqServerName>[^ ]+)"
    r" (?P<RouteName>[^ ]+)"  # 'default'
    # r' "(?P<EndpointMethod>\w+)'
    # r' (?P<EndpointPath>[^ ]+)"'
    # r" (?P<ServiceTracing>([_\w\d\-]+\(\d+\)\|)+)"
)


def message_parser(raw_text: str):
    raw_text = raw_text.replace("\n", "")
    matched = re.match(match_pattern, raw_text)
    if matched is None:
        print("Err", raw_text)
        return None
    return matched.groupdict()


def test():
    # raw_txt = """[2022-05-25T06:38:13.956Z] "GET / HTTP/1.1" 200 - via_upstream - "-" 0 35430 6 6 "-" "Python/3.9 aiohttp/3.8.1" "e4c5583b-565c-9026-8e5d-974bdf8ab467" "service2.prod:4000" "10.42.2.204:4000" inbound|4000|| 127.0.0.6:56089 10.42.2.204:4000 10.42.3.252:54568 - default "GET /" service2(200)|"""
    # raw_txt = """[2022-05-25T06:38:13.956Z] "GET / HTTP/1.1" 200 - via_upstream - "-" 0 35430 6 6 "-" "Python/3.9 aiohttp/3.8.1" "e4c5583b-565c-9026-8e5d-974bdf8ab467" "service2.prod:4000" "10.42.2.204:4000" inbound|4000|| 127.0.0.6:56089 10.42.2.204:4000 10.42.3.252:54568 - default "GET /" service2(200)|service3(200)|"""
    raw_txt = """[2022-11-10T07:53:51.283Z] "- - -" 0 - - - "-" 3505 2337 5051 - "-" "-" "-" "-" "10.42.0.254:8000" inbound|8000|| 127.0.0.6:48119 10.42.0.254:8000 10.42.0.247:56434 outbound_.4000_._.front-app.front.svc.cluster.local -"""
    print(raw_txt)

    result = message_parser(raw_txt)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=pathlib.Path, dest="filepath")
    args = parser.parse_args()
    
    buffer = []
    with open(args.filepath) as f:
        while (line := next(f, None)) is not None:
            x = message_parser(line)
            buffer.append(json.dumps(x))

    buffer = "\n".join(buffer)
    with open(f"{args.filepath}.parsed", mode='w') as f:
        f.write(buffer)


if __name__ == "__main__":
    #test()
    main()
