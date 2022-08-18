# memo

1dayのログの平均的なデータサイズを調べた．

```
cat 1day.csv | awk -F, '{print $4}' | sed 's/""/"/g' | awk 'BEGIN{total=0} {total+=length($0)}END{print total/NR}'
332.806
```

結果は 333 文字で 333[KB] が平均の1件のログあたりのデータサイズだとわかった．
