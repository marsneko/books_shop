#博客來書籍資料收集

## 排行榜資料

---
### 爬取排行榜資料
- `topsales.py`:依類別爬取博客來的銷售排行榜，並將其依序儲存至`topSales`, 
`preSales`, `newSales`資料夾中。
- `mergeToCsv.py`:將`topSales`, `preSales`, `newSales`資料夾中的資料合併成 csv 檔，於
`./data`資料夾中。
- `addDate.py`:將`./data`資料夾中的 csv 檔加上日期欄位，並儲存至`./Datedata`資料夾中。
- `topsalesbookdata.py`:將`./Datedata`中資料加入其書籍的出版日期與出版社等資料，並儲存至`./book_info`資料夾中。

### 分析結果
- 主要使用`topsalesAnalysis.py`進行分析，部分結果儲存至`pic`資料夾中。
- 