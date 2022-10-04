Istio Proxyのメッセージ形式を拡張する．

https://istio.io/latest/docs/tasks/observability/logs/access-log/

デフォルトのログ形式は以下になる．

```
[%START_TIME%] \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS% \"%UPSTREAM_TRANSPORT_FAILURE_REASON%\" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% \"%REQ(X-FORWARDED-FOR)%\" \"%REQ(USER-AGENT)%\" \"%REQ(X-REQUEST-ID)%\" \"%REQ(:AUTHORITY)%\" \"%UPSTREAM_HOST%\" %UPSTREAM_CLUSTER% %UPSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_REMOTE_ADDRESS% %REQUESTED_SERVER_NAME% %ROUTE_NAME%\n
```

具体的なフォーマットは以下である．

```
2022-07-13T03:38:52.810Z,GET,/stats,HTTP/1.1,200,"- via_upstream - ""-""",0 14759 16 16,-,Python/3.9 aiohttp/3.8.1,0efb8f3e-8aaf-48b7-a5eb-ec3a7375d78b,stats-app.stats:4000,10.42.0.21:8000,inbound|8000||,127.0.0.6:59785,10.42.0.21:8000,10.42.0.23:55876,outbound_.4000_._.stats-app.stats.svc.cluster.local,default
```

ログフォーマットを拡張を考える．Istio ProxyはEnvoyで実装されているのでEnvoyのドキュメントからアクセスログの形式について調べる．

https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#format-rules

> %REQ(X?Y):Z%
>
> HTTP
>
> An HTTP request header where X is the main HTTP header, Y is the alternative one, and Z is an optional parameter denoting string truncation up to Z characters long. The value is taken from the HTTP request header named X first and if it’s not set, then request header Y is used. If none of the headers are present ‘-‘ symbol will be in the log.

独自のヘッダをログ形式に追加する場合は， `%REQ(X?Y):Z%` を使えばよい．

```
\"%REQ(X-ENDPOINT-METHOD)% %REQ(X-ENDPOINT-PATH)%\"
```

- x-endpoint-method
- x-endpoint-path
- x-service-tracing