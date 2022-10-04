# memo

1dayのログの平均的なデータサイズを調べた．

```
cat 1day.csv | awk -F, '{print $4}' | sed 's/""/"/g' | awk 'BEGIN{total=0} {total+=length($0)}END{print total/NR}'
332.806
```

結果は 333 文字で 333[KB] が平均の1件のログあたりのデータサイズだとわかった．

Pythonで確かめた．

```
cat 1day.csv | awk -F, '{print $4}' | sed 's/""/"/g' | awk '{print length($0)}' > a

$ python
>>> with open("a") as f:
...     ls = f.read().splitlines()
...
>>> map(int, ls)
<map object at 0x102fd9c70>
>>> sum(map(int, ls))
6677424
>>> sum(map(int, ls)) // len(ls)
332
>>> sum(map(int, ls)) / len(ls)
332.8062200956938
```
