## 批量下载文件

### 单个下载页面

支持批量下载页面中的多个下载链接。

至少需要配置 `downloader_main_url` 和 `downloader_download_links`

### 多个下载页面

支持从下载汇总页面跳转至下载页面，再批量下载页面中的多个下载链接

至少需要配置 `downloader_main_url` , `downloader_download_links` , `downloader_follow_links`

### 下载文件的命名方式

* 使用下载链接的名字来命名
* 使用下载页面的 Title 结合数字编号来命名
* 使用下载链接的 md5(URL) 结合数字编码来命名
* 使用网站为下载资源指定的文件名来命名