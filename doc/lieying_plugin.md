:: lieying_plugin.md, language *Chinese* (`zh_cn`)
:: *last_update* `2015-07-11 19:29 GMT+0800 CST`

# 猎影插件接口定义 version 0.2.0-test.1

author: `sceext <sceext@foxmail.com>`

此文件用来说明 猎影插件接口 的定义. 


## 内容目录

+ **[0. 基本说明](#0-基本说明)**
  
  + **[0.1 猎影](#01-猎影)**
  + **[0.2 猎影插件](#02-猎影插件)**
  + **[0.3 猎影插件接口](#03-猎影插件接口)**

+ **[1. 猎影插件的格式](#1-猎影插件的格式)**
  
  + **[1.1 编程语言 (`python3`)](#11-编程语言-python3)**
  + **[1.2 打包格式 (`zip`)](#12-打包格式-zip)**
  + **[1.3 入口文件 (`run.py`)](#13-入口文件-runpy)**
  + **[1.4 接口函数](#14-接口函数)**
  + **[1.5 错误处理](#15-错误处理)**

+ **[2. 猎影插件接口函数定义](#2-猎影插件接口函数定义)**
  
  + **[2.1 `GetVersion()`](#21-getversion)**
  + **[2.2 `StartConfig()`](#22-startconfig)**
  + **[2.3 `Parse()`](#23-parse)**
  + **[2.4 `ParseURL()`](#24-parseurl)**

+ **[3. 示例](#3-示例)**


## 0. 基本说明

### 0.1 猎影

**猎影** 是一款 视频下载软件, 能够下载许多 在线视频网站 的视频. 
并且 界面 简洁美观, 方便易用. 

猎影 的 **官方网站** 是 <http://lieying.ilewo.cn/>

### 0.2 猎影插件

**猎影插件** 是 *猎影* 的 *插件*, 是为了 **补充** 或 **增强** 猎影的功能. 

目前支持的 插件类型 有:

+ **解析插件** (*parse*)
  
  *解析插件* 提供 **解析** 功能. 
  
  即 输入 视频网站页面的 URL, 或者 视频名称 等, 
  由 解析插件 解析出 视频文件的下载地址, 视频标题 等信息. 
  
  然后 由猎影进行下载. 

### 0.3 猎影插件接口

**猎影插件接口** 就是 *猎影* 和 *猎影插件* 之间定义的接口. 

*猎影插件接口* 使用 **语义化版本**号 (semver 2.0.0, <http://semver.org/lang/zh-CN/>) 
来定义 接口 的版本, 以便处理 兼容性, 功能更新 等问题. 


## 1. 猎影插件的格式

### 1.1 编程语言 (`python3`)

*猎影插件* 使用 **[python3](https://docs.python.org/3/)** 作为 编程语言. 

*猎影* 会附带 **完整**的 `python 3.4` 运行环境, 包括 标准库, 和默认随 `python3` 安装的软件包. 
但是不附带其他使用 `pip` 安装的软件包. 

### 1.2 打包格式 (`zip`)

*猎影插件包* 是标准的 `zip` 格式的 **压缩包**. 
压缩包 中可包含任意数量的 文件, 其中只有一个 `run.py` 即 猎影插件的**入口文件**, 是**必须**的. 

### 1.3 入口文件 (`run.py`)

`run.py` 是 *猎影插件* 的 **入口文件**. 
`run.py` **必须**位于 压缩包 的**指定位置**. 

在 **指定位置** 只能有 1 个 `run.py` 文件. 

`run.py` 可用的 **指定位置** 有:

+ 压缩包 **根目录** 下 
+ 压缩包 根目录 下只有一个文件夹, 且 `run.py` 位于此 唯一 的文件夹下 

**比如**: 
`run.py` 有如下 2 种位置:

**1.** 假设 插件压缩包 根目录 为 `root`
```
 - root/
     run.py 
```

**2.** 假设 根目录 下只有一个 `plugin` 文件夹
```
 - root/
     - plugin/
         run.py
```

### 1.4 接口函数

`run.py` 中定义有若干 **接口函数**. 

使用 插件 时, 猎影会先 **导入** `run.py` 这个 python 模块, 然后调用其中的函数. 

**举例说明**: 猎影导入 `run.py` 的动作 相当于 python 中的 `import run`, 
调用其中 `GetVersion()` 函数的动作相当于 python 中的 `run.GetVersion()` 

目前定义的 接口函数 有:

+ `GetVersion()`
+ `StartConfig()`

> 

+ `Parse()`
+ `ParseURL()`

具体的 函数定义, 包括 参数, 返回值, 功能说明, 等, 请见下文. 

### 1.5 错误处理

<!-- TODO -->


## 2. 猎影插件接口函数定义

### 2.1 `GetVersion()`

([`GetVersion()` 示例](#32-测试-getversion))

+ **函数定义**
  
  ```
  def GetVersion()
  ```
  **注意**: 所有类型的插件都必须定义该接口函数. 

+ **功能说明**

+ **参数**
  
  **无** <br />
  此函数没有定义参数. 

+ **返回值**

**`json` 字符串**

<!-- TODO -->

+ **更多说明**

### 2.2 `StartConfig()`

(`StartConfig()` 没有示例)

+ **函数定义**
  
  ```
  def StartConfig()
  ```
  **注意**: 所有类型的插件都必须定义该接口函数. 

+ **功能说明**

+ **参数**
  
  **无** <br />
  此函数没有定义参数. 

+ **返回值**
  
  **无** <br />
  此函数没有定义返回值. 

+ **更多说明**

### 2.3 `Parse()`

([`Parse()` 示例](#33-测试-parse))

+ **函数定义**
  
  ```
  def Parse(input_text)
  ```
  **注意**: 以下类型的插件需要定义此接口函数:
  + `parse` 解析插件

+ **功能说明**

+ **参数**
  
  + **`input_text`**

+ **返回值**
  
  **`json` 字符串**

<!-- TODO -->

+ **更多说明**

### 2.4 `ParseURL()`

([`ParseURL()` 示例](#34-测试-parseurl))

+ **函数定义**
  
  ```
  def ParseURL(url, format, i_min=None, i_max=None)
  ```
  **注意**: 以下类型的插件需要定义此接口函数:
  + `parse` 解析插件

+ **功能说明**

+ **参数**
  
  + **`url`**
  
  + **`format`**
  
  + **`i_min`**
  
  + **`i_max`**

+ **返回值**
  
  **`json` 字符串**

<!-- TODO -->

+ **更多说明**


## 3. 示例

### 3.1 导入插件, 其他初始化工作

```
$ python
Python 3.4.3 (default, Mar 25 2015, 17:13:50) 
[GCC 4.9.2 20150304 (prerelease)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import run
>>> import json
>>> def p(o):
...     print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))
... 
>>> 

```

其中定义的 p() 函数, 用于解析插件返回的 json 字符串, 并重新打印出来. 

### 3.2 测试 `GetVersion()`

```
>>> v = run.GetVersion()
>>> p(v)
{
    "author": "sceext <sceext@foxmail.com>",
    "copyright": "copyright 2015 sceext All rights reserved. ",
    "filter": [
        "^http://[a-z]+\\.iqiyi\\.com/.+\\.html"
    ],
    "home": "https://github.com/sceext2/parse_video/tree/output-easy",
    "license": "GNU GPLv3+",
    "name": "parse_video_7lieying_plugin57 (plugin version 0.11.2, kernel version 0.3.5.1) license GNU GPLv3+ ",
    "type": "parse",
    "uuid": "ebd9ac19-dec6-49bb-b96f-9a127dc4d0c3",
    "version": "0.11.2"
}
>>> 

```

### 3.3 测试 `Parse()`

### 3.4 测试 `ParseURL()`


<!-- TODO -->

:: end lieying_plugin.md, <https://github.com/sceext2/lieying_plugin>


