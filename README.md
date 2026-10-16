# WenKu8-Downloader

一个简易小说txt下载器，来源WenKu8。此站前端鉴权，后端裸奔，接口来源来自URL猜测。

最近在看番和原著小说，WenKu8的web端下载要登录。

不得不说，这番真好看。

接口来源：
```
www.wenku8.net/*        → 403 (Cloudflare WAF)
app.wenku8.com/android.php → 502 (后端死了)
    ↓ 猜测同架构兄弟子域
dl.wenku8.com/down.php?type=utf8&id=2586 → 200 全本
dl.wenku8.com/packtxt.php → 200 单章
img.wenku8.com / m.wenku8.net → 403 / 502
```
