<h1 align="center"><i>✨ onebot-plugin-files ✨ </i></h1>

<h3 align="center"> 同步群文件 </h3>

[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-files.svg)](https://pypi.org/project/nonebot-plugin-files/)
![python](https://img.shields.io/pypi/pyversions/nonebot-plugin-files)
![implementation](https://img.shields.io/pypi/implementation/nonebot-plugin-files)
![wheel](https://img.shields.io/pypi/wheel/nonebot-plugin-files)
![license](https://img.shields.io/github/license/synodriver/nonebot-plugin-files.svg)
![action](https://img.shields.io/github/workflow/status/synodriver/nonebot-plugin-files/build%20wheel)

### install
```bash
pip install nonebot-plugin-files
```

### 配置
```angular2html
SYNC_ALLOW_BOTS=["123"]  # 允许进行同步的bot
STORAGE_PATH="/home/lighthouse" # 保存文件根目录
```

### 使用
```angular2html
同步 -g 群号 -t 下载器类型

```
- 群聊可以不给群号参数，此时就是发出指令的这个群
- 下载器类型：
- 
1. download: BaseDownloadHandler， 普通下载
2. aria2: Aria2DownloadHandler, 使用aria2下载
3. "ftp": FTPUploadHandler, 下载了上传到ftp
4. "webdav": WebDavUploadHandler, 下载了上传到webdav
5. "log": LogFileHandler, 记录但是不下载
6. "test": MockHandler 仅在console输出log