# istio-log-analysis

istioログの例とパーサ

## 構成ファイル群

- extend.py: Elasticsearchからエクスポートした拡張前CSVファイルを読み込み，形式を拡張する．結果をCSV形式(拡張済みCSVファイル)に保存する．
- parser.py: 拡張前ログ形式をパースする．他のコードからこのファイルを読み込んで使う．
- analyzer.py: Elasticsearchからエクスポートした拡張前CSVファイルを読み込んで要約した結果を標準出力へ書き出す．
- reducer.py: 拡張済みCSVファイルを読み込んで要約した結果を標準出力へ書き出す．

## ログについて

- logs-v1/ の中身はリクエストIDが1トランザクションに対応していない．つまり，1トランザクションに複数個のIDが付与されている．
- logs-v2/ の中身はリクエストIDが1トランザクションに対応している．つまり，1トランザクションに1個のIDが付与されている．

## メモ

計測対象のデータ

20220719-082129_1day-ext.csv_30_DateTime,EndpointMethod,EndpointPath,ServiceTracing.log
