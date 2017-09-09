google-crawler.py：使用google API得到台股收盤價，更新於stockReturn資料夾。
cloud_scheduler.py：自動化每日定時執行cloud.sh以更新資料。
cloud.sh：執行所有後台模型資料更新及上傳的python檔案。
ID.csv：儲存台股前50大個股ID。
predict.py：分析每日新聞。
merge.py：預測模型，配合predict.py程式預測個股趨勢。
upload_price.py：上傳台股前50大個股之預測結果。
upload.py：上傳news中每日新聞。
upload_history.py：上傳所有股票的股價、新聞、及預測結果。
news：存放每日新聞。路徑為"news/YYYY/mm/YYYYmmdd/"。檔名格式
"[YYYYmmdd][Title]##股票代號.txt"。
newsPNV：存放預測模型中predict.py的結果。
merge：存放預測模型中merge.py的結果。
openfire_4.0.3_all.deb：openfire主程式安裝檔。
xampp-linux-x64-7.0.9-1-installer.run：xampp伺服器程式安裝檔。
Stock.sql：資料庫格式，可直接透過phpmyamdin匯入。
系統流程.txt：系統流程介紹。
安裝流程.txt：建構系統流程說明，搭配技轉過程之指令除錯。
NCCUStock_app.apk：技轉過程中內部測試apk。
20170221_terminal_note&20170221_terminal_note：技轉兩日之完整指令紀錄。


預測模型使用程式(不主動執行)：
FileToList.py
GetFilePaths.py
GetFilePaths.pyc
FileToList.pyc
預測模型使用資料：
financeReport
prepareFile
stock_price
stockReturn

