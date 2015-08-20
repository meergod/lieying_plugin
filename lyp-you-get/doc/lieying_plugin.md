:: lieying_plugin.md, language *Chinese* (`zh_cn`)
:: *last_update* `2015-07-16 12:08 GMT+0800 CST`

# 猎影插件接口定义 version 0.2.1

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
  + **[1.5 文本格式 (*单行文本*, *多行文本*)](#15-文本格式)**
  + **[1.6 错误处理](#16-错误处理)**

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

具体的 函数定义, 包括 参数, 返回值, 功能说明, 等, 请见[下文](#2-猎影插件接口函数定义). 

### 1.5 文本格式

在此 **明确定义** *猎影插件接口* 有关 *文本格式* 使用的 
2 个 概念, **单行文本** 和 **多行文本**. 

+ **编码** (`utf-8`)
  
  *猎影插件接口* 使用的 **文本** *(字符串)*, 全部使用 **`utf-8`** **编码**. 

+ **单行文本**
  
  **只有** 1 行 的文本. *文本 字符串* 中 **不允许 出现** `\r` 或 `\n` 字符. 
  
  **注**: 此处所说的 `\r` 和 `\n` 字符, 即 `python` 中定义的 *转义字符*. 
  如下所示: 
  
  ```
  >>> ord('\r')
  13
  >>> ord('\n')
  10
  >>> 
  ```

+ **多行文本**
  
  **可以** 有 多行 的文本. 
  注意, 是可以有多行, 在能够使用 *多行文本* 的位置, 
  都可以使用 *单行文本*. 
  
  *多行文本* 的 *文本 字符串* 使用 `\n` 表示换行. 
  
  也就是说, *多行文本 字符串* 中 **允许** 出现 `\n`, 但是 **不允许** 出现 `\r`. 

### 1.6 错误处理

当插件的 *接口函数* 执行中遇到错误, 请使用 `python` 的 `raise` 语句抛出一个错误. 

猎影会 **显示详细的错误信息**. 

比如

```
raise Exception('can not load page: http 404')
```

建议抛出错误时, 尽可能给出有用的详细错误信息, 以便帮助调试. 

**注意**: 抛出错误的 描述信息 *字符串* **允许**使用 **多行文本**, 


## 2. 猎影插件接口函数定义

### 2.1 `GetVersion()`

([`GetVersion()` 示例](#32-测试-getversion))

+ **函数定义**
  
  ```
  def GetVersion()
  ```
  **注意**: **所有类型**的插件都**必须**定义此接口函数. 

+ **功能说明** <br />
  用于返回插件的版本号等有关信息. 
  具体返回的信息及其格式, 请见 *返回值* 说明. 

+ **参数**
  
  **无** <br />
  此函数没有定义参数. 

+ **返回值**
  
  类型: **`json` 字符串**
  
  json 信息结构: 
  
  ```
  {
      "port_version" : "0.2.1", 
      "type" : "", 
      "uuid" : "", 
      "version" : "", 
      "name" : "", 
      
      "filter" : [], 
      
      "author" : "", 
      "copyright" : "", 
      "license" : "", 
      "home" : "", 
      "note" : ""
  }
  ```
  
  以下项目, **所有类型**的插件都**必须**定义: 
  
  + **`port_version`** 类型: 字符串 *(单行文本)* <br />
    插件所使用的 *猎影插件接口* 的 **版本号**. 
    
    [当前](#03-猎影插件接口) 版本号是 `0.2.1`
  
  + **`type`** 类型: 字符串 *(单行文本)* <br />
    插件类型. 
    
    目前支持的 [插件类型](#02-猎影插件) 有
    
    + **`parse`**: 解析插件
  
  + **`uuid`** 类型: 字符串 *(单行文本)* <br />
    插件的 `uuid` 标识. 
    
    猎影 将**仅根据** *uuid* 来识别一个插件, 而不用 *插件名称* 等其它信息. 
    就是说, 只要 uuid 相同, 猎影就会认为这是同一个插件. 
    
    开始写一个 *猎影插件* 时, 应该使用 uuid 生成软件 (比如 `uuidgen`) 为此 插件 生成一个 `uuid`. 
    
    在发布插件的新版本时, **除非故意**这么做, 否则**不要修改**此插件的 *uuid*. 
    猎影会提示插件升级, 并且使用 新版插件 替换 旧版插件. 
  
  + **`version`** 类型: 字符串 *(单行文本)* <br />
    插件 版本号. 
    
    这个是 插件 自己的 版本号. 
    使用何种版本号规范, 由插件自己决定. 
    *猎影插件接口* 不做统一规定. 
  
  + **`name`** 类型: 字符串 *(单行文本)* <br />
    插件名称. 
    
    这个 *插件名称* 将显示在 *猎影* 的 *插件列表* 中. 
    
    **注意**: 猎影 不使用 *插件名称* 来唯一识别一个插件, 而是使用 `uuid`. 
  
  
  以下项目, 类型为 **`parse`** *(解析插件)* 的插件, **需要**定义. 
  
  + **`filter`** 类型: 数组 (`list`, `[]`, `Array`) <br />
    返回 `Parse()` 函数 支持的 文本输入的 *正则表达式* 数组. 
    数组内容为 字符串, 每个字符串 是一个 正则表达式. 
    
    在调用插件的 `Parse()` 函数之前, 猎影会 尝试 使用 `filter` 数组中的 
    *正则表达式* 匹配 *输入的字符串*. 如果匹配, 将会调用 此插件, 否则不会. 
  
  
  以下项目, **所有类型** 的插件都 **可以** 定义, 也就是说, 是 *可选*的项目, 不是必须定义. 
  
  + **`author`** 类型: 字符串 *(多行文本)* <br />
    插件 的 作者信息. 
  
  + **`copyright`** 类型: 字符串 *(多行文本)* <br />
    插件 的 版权信息. 
  
  + **`license`** 类型: 字符串 *(多行文本)* <br />
    插件 使用的 **许可证** (*license*). 
    
    比如 `GNU GPLv3+`, `MIT`, `unlicense`, 等. 
  
  + **`home`** 类型: 字符串 *(多行文本)* <br />
    插件 的 首页地址. 
    
    可以是 插件的 官方网站, 插件的 github 项目主页, 等. 
  
  + **`note`** 类型: 字符串 *(多行文本)* <br />
    插件 的 描述信息. 

+ **更多说明**
  
  + 插件可以在 `GetVersion()` 的返回的结果中 自己添加 一些其它的信息. 
    然而, 猎影 并不保证会使用这些信息, 猎影 可能直接忽略它们. 
    
    但是, 已经被 *猎影插件接口* 定义的项目, **必须**按照 *猎影插件接口* 定义的方式使用. 

### 2.2 `StartConfig()`

(`StartConfig()` 没有示例)

+ **函数定义**
  
  ```
  def StartConfig()
  ```
  **注意**: **所有类型**的插件都**可以**定义此接口函数. 

+ **功能说明** <br />
  用于启动插件自带的配置程序. 
  
  猎影插件管理界面, 会提供 *配置插件* 按钮. 
  用户点击此按钮之后, 猎影会调用此函数, 通知插件用户想要启动配置程序. 
  
  剩下的全部事情, 由插件自己处理. 

+ **参数**
  
  **无** <br />
  此函数没有定义参数. 

+ **返回值**
  
  **无** <br />
  此函数没有定义返回值. 

+ **更多说明**
  
  + 建议使用 python3 自带的 [`tkinter`](https://docs.python.org/3/library/tk.html) 
    组件提供图形界面的配置程序. 
  
  + 如果插件**不支持配置**, 或者没有自带的配置程序, 请**不要定义** `StartConfig()` 函数. 
    
    这样猎影的插件管理界面, 就不会再显示 *配置插件* 按钮. 
  
  + 插件可以自行使用配置文件保存配置信息. 配置文件可以与插件的 python 代码放在一起. 
    
    猎影不会处理插件配置信息的保存, 插件需要自行处理. 

### 2.3 `Parse()`

([`Parse()` 示例](#33-测试-parse))

+ **函数定义**
  
  ```
  def Parse(input_text)
  ```
  **注意**: 以下类型的插件需要定义此接口函数:
  + `parse` (解析插件)

+ **功能说明** <br />
  解析 *用户输入的字符串*, 返回解析结果. 
  
  用户输入的文本, 可能是一个 URL, 也可能是 视频名称 等其它信息. 
  这取决于 `GetVersion()` 返回信息中 `filter` *正则表达式* 的定义. 
  
  根据不同的 用户输入, 插件可自行选择一种 解析模式. 
  目前支持的 **解析模式** 有:
  
  + **单视频解析** <br />
    用户输入的文本, 应该解析出**一个**视频. <br />
    此时, 返回 这个视频的若干可选的 不同格式, 供用户选择. 
    
    比如, 用户输入 某一集 电视剧 播放网页的 URL, 
    此时可以解析出 1080p, 720p 等不同格式的视频. 
  
  + **多视频解析** <br />
    用户输入的文本, 应该解析出**多个**视频. <br />
    此时, 返回 若干 视频项目, 供用户选择. 
    
    比如, 用户输入 某一部 电视剧 剧集页面的 URL, 
    此时可以解析出 每一集 电视剧 播放页面 的 URL. 

+ **参数**
  
  + **`input_text`** 类型: 字符串 *(单行文本)* <br />
    用户输入的字符串. 

+ **返回值**
  
  类型: **`json` 字符串**
  
  *单视频解析*模式, 和 *多视频解析*模式, 返回结果是不一样的. 
  
  **单视频解析**
  
  json 信息结构: 
  
  ```
  {
      "type" : "formats", 
      "name" : "", 
      "data" : [
          {
              "label" : "", 
              "ext" : "", 
              "size" : ""
          }
      ]
  }
  ```
  
  + **type** 类型: 字符串 *(单行文本)* <br />
    返回结果的类型, 值 **必须** 为 `formats`, 表示这是 *单视频解析* 的结果. 
  
  + **name** 类型: 字符串 *(单行文本)* <br />
    视频的标题. 
    
    *视频标题* 的具体文本格式, 由插件自行处理, *猎影插件接口* 不做统一规定. 
  
  + **data** 类型: 数组 (`list`, `[]`, `Array`) <br />
    *视频格式* 信息. 
    
    数组内容为若干 `dict` (`{}`, `Object`). 
    每个 `dict` 表示一种视频的格式. 
  
  + **label** 类型: 字符串 *(单行文本)* <br />
    格式说明字符串. 用来表示并区分不同的视频格式. 
    
    猎影会在列表中显示 此字符串, 供用户选择. 
    
    `label` *字符串* 的格式由插件自行处理, *猎影插件接口* 不做统一规定. 
  
  + **ext** 类型: 字符串 *(单行文本)* <br />
    视频文件的扩展名. 用来表示这种格式视频的 视频文件格式. 
    
    比如 `mp4`, `flv`, 等. 
  
  + **size** 类型: 字符串 *(单行文本)* <br />
    此种格式视频的文件大小 (如果有多个视频文件, 指它们的总大小). 
    
    以方便用户阅读的格式提供, 比如 `1.01 GB`. 
  
  
  **多视频解析**
  
  json 信息结构:
  
  ```
  {
      "type" : "list", 
      
      "title" : "", 
      "total" : -1, 
      "more" : false, 
      
      "data" : [
          {
              "no" : "", 
              "subtitle" : "", 
              "name" : "", 
              "url" : ""
          }
      ]
  }
  ```
  
  + **type** 类型: 字符串 *(单行文本)* <br />
    返回结果的类型, 值 **必须** 为 `list`, 表示这是 *多视频解析* 的结果. 
  
  + **title** 类型: 字符串 *(单行文本)* <br />
    这些视频的 整体标题. 
    
    比如, 解析结果是 某部电视剧的 每一集, 那么 此标题, 可选为 这部电视剧的 名称, 不包含 第几集. 
    
    如果 不便给出此标题, 可以返回 `""` *(空字符串)*. 
    
    `title` *字符串* 的格式由插件自行处理, *猎影插件接口* 不做统一规定. 
  
  + **total** 类型: 整数 <br />
    这些视频的 总数. 
    
    比如, 解析结果是 某部电视剧的 40集, 这里总数应该返回 40. 
    
    如果 不知道, 应该返回 `-1`. 
  
  + **more** 类型: `bool` (`boolean`) <br />
    是否能够返回更多结果. 
    
    如果没有更多结果, 应返回 `false`. 
    
    如果有更多结果, 应返回 `true`. 
    返回 `true` 之后, 猎影 **可能** 会再次调用 `Parse()` 获取更多结果. 
  
  + **data** 类型: 数组 (`list`, `[]`, `Array`) <br />
    *视频项目* 信息. 
    
    数组内容为若干 `dict` (`{}`, `Object`). 
    每个 `dict` 表示一个视频项目. 
  
  + **no** 类型: 字符串 *(单行文本)* <br />
    能简短的 将此视频 区别出来 的字符串. 
    
    比如, 解析结果是 某部电视剧的每一集, 此处可以使用 *第x集* 这种形式. 
    
    `no` *字符串* 的具体格式, 由插件自行处理, *猎影插件接口* 不做统一规定. 
  
  + **subtitle** 类型: 字符串 *(单行文本)* <br />
    此视频的 **小标题**. 
    
    比如, 有些视频网站, 给电视剧的每一集, 都加一个 *小标题*. 
    
    如果 不便给出, 可以返回 `""` *(空字符串)*. 
    
    `subtitle` *字符串* 的格式由插件自行处理, *猎影插件接口* 不做统一规定. 
  
  + **name** 类型: 字符串 *(单行文本)* <br />
    此视频的 **完整标题**. 
    
    此处的 `name` 应该和 *单视频解析* 时, 解析这个视频返回的 `name` *字符串* 保持一致. 
  
  + **url** 类型: 字符串 *(单行文本)* <br />
    此视频的 URL. 
    
    当进行 *单视频解析* 时, 此字符串会被 **按原样** 传入 `Parse()` 的 `input_text` 参数. 

+ **更多说明**
  
  + 当返回 *多视频解析* 结果后, 猎影 很可能会再次调用 `Parse()` 进行 *单视频解析*, 
    且传入的 `input_text` 就是 *多视频解析* 返回的 `url`. 
  
  + 所以, *多视频解析* 返回的 `url` *字符串*, 不一定必须是 URL. 也可以是其它格式. 
    只要插件 在进一步的 *单视频解析* 中能够识别处理 即可. 

### 2.4 `ParseURL()`

([`ParseURL()` 示例](#34-测试-parseurl))

+ **函数定义**
  
  ```
  def ParseURL(url, label, i_min=None, i_max=None)
  ```
  **注意**: 以下类型的插件需要定义此接口函数:
  + `parse` (解析插件)

+ **功能说明** <br />
  解析 视频文件的 **下载地址**. 
  
  当调用 `Parse()` 进行 *单视频解析* 并且获取 视频格式 后, 
  猎影 会调用 `ParseURL()` 解析视频文件的下载地址, 然后进行下载. 

+ **参数**
  
  + **`url`** 类型: 字符串 *(单行文本)* <br />
    此字符串与调用 `Parse()` 进行 *单视频解析* 时传入的 `input_text` 相同. 
  
  + **`label`** 类型: 字符串 *(单行文本)* <br />
    此字符串与调用 `Parse()` 进行 *单视频解析* 时返回结果中的一个 `label` *字符串* 相同. 
    表示需要解析此种格式视频的文件下载地址. 
  
  + **`i_min`** 类型: 整数 或 `None` <br />
    **希望获取**的 分段文件信息的 **最小 序号**, 按数组下标, 0 表示第 1 段. 
    
    若为 `None` 表示不加限制. 
  
  + **`i_max`** 类型: 整数 或 `None` <br />
    **希望获取**的 分段文件信息的 **最大 序号**, 按数组下标, 0 表示第 1 段. 
    
    若为 `None` 表示不加限制. 

+ **返回值**
  
  类型: **`json` 字符串**
  
  json 信息结构: 
  
  ```
  [
      {
          "protocol" : "http", 
          "args" : {}, 
          "value" : ""
      }
  ]
  ```
  
  返回的 json 结果, 整体是一个 数组 (`list`, `[]`, `Array`), 
  数组的每一项是一个 `dict` (`{}`, `Object`). 
  
  每个 `dict` 表示一个 **分段视频文件** 的*下载信息*. 
  
  之所以这样设计, 是因为 有许多视频, 都是**分段视频**, 需要下载所有 *分段视频文件*, 
  并且 *合并* 之后, 才能得到完整的视频. 
  
  + **protocol** 类型: 字符串 *(单行文本)* <br />
    下载使用的 *协议*. 
    
    目前支持以下协议: 
    
    + **`http`**
  
  + **args** 类型: `dict` (`{}`, `Object`) <br />
    下载协议所需的额外信息. 
    
    + 对于 `http` 协议, `args` 是额外的 **http 头**. 
      
      比如 `User-Agent`, `Referer`, 等. 
      
      如果不需要定义 额外的 *http 头*, 应该返回 `{}` *(空 `dict`)*. 
  
  + **value** 类型: 字符串 *(单行文本)* <br />
    下载地址. 
    
    + 对于 `http` 协议, 是类似于 `http://` 这样的字符串. 

+ **更多说明**
  
  `ParseURL()` 以 数组 格式返回下载信息, 对于 分段视频, 
  **插件一定要保证返回的分段文件的顺序正确 !!!**
  
  比如, 一个 10 分钟的视频, 被分成 2 段, 第 1 段是 0 至 6 分钟, 第 2 段是 7 至 10 分钟, 
  那么 插件返回的下载信息数组, 一定要保证 第 1 段 在 第 2 段 的前面. 
  
  猎影会 按照插件返回的 分段文件顺序 合并视频. 
  如果插件返回的顺序不正确, 将会导致 合并后的视频 **播放时间错乱 !!!**

+ **对 `i_min` `i_max` 参数的说明**
  
  `i_min` 和 `i_max` 参数, 用于 *猎影插件* 的一个 **高级特性**: **逐个解析**. 
  
  简单来说, 就是猎影每调用一次 `ParseURL()` 将 
  只 解析并返回 1 个 或 仅仅几个 分段文件的下载信息, 
  而不是返回全部. 
  
  只有在 **解析较慢** 的情况下, 此特性才有明显的效果. 
  
  **多数情况**下, 不需要使用此特性, 可以**直接忽略** `i_min` 和 `i_max` 参数. 
  
  并且, 即使插件 **忽略** `i_min` 和 `i_max` 参数, 也**不会造成任何错误**, 
  *猎影* 以及 *猎影插件* 仍然能够正常工作. 
  
  不过, 如果支持此特性, 在某些情况下, 能够获得更好的性能. 
  
  由于 `i_min` 和 `i_max` 参数 稍显 复杂, 在此不再 详细说明. 
  如有需要, 请阅读 
  [lieying_plugin_ParseURL.md](https://github.com/sceext2/lieying_plugin/blob/plugin-you-get/doc/lieying_plugin_ParseURL.md)
  获取更多详细信息. 


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
    "copyright": "copyright 2015 sceext",
    "filter": [
        "^http://[a-z]+\\.iqiyi\\.com/.+\\.html"
    ],
    "home": "https://github.com/sceext2/parse_video/tree/output-easy",
    "license": "GNU GPLv3+",
    "name": "parse_video_10lieying_plugin60 (plugin version 0.14.0, kernel version 0.3.5.1) license GNU GPLv3+ ",
    "note": "A parse plugin for lieying with parse support of parse_video. ",
    "port_version": "0.2.0",
    "type": "parse",
    "uuid": "ebd9ac19-dec6-49bb-b96f-9a127dc4d0c3",
    "version": "0.14.0"
}
>>> 
```

### 3.3 测试 `Parse()`

*多视频解析* 测试

```
>>> a = run.Parse('http://www.iqiyi.com/a_19rrhb16x1.html')
pvtkgui: DEBUG: vlist.entry: load page "http://www.iqiyi.com/a_19rrhb16x1.html"
pvtkgui: DEBUG: vlist.entry: parse info
>>> p(a)
{
    "data": [
        {
            "name": "_0001_花千骨未删减版第1集_画骨夫妇初相遇__不可说",
            "no": "第1集_画骨夫妇初相遇",
            "subtitle": "画骨夫妇初相遇",
            "url": "http://www.iqiyi.com/v_19rroiitws.html"
        },
        {
            "name": "_0002_花千骨未删减版第2集_尊上圣君霸气对垒__不可说",
            "no": "第2集_尊上圣君霸气对垒",
            "subtitle": "尊上圣君霸气对垒",
            "url": "http://www.iqiyi.com/v_19rroiiwig.html"
        },
        {
            "name": "_0003_花千骨未删减版第3集_闯关考核为长留__不可说",
            "no": "第3集_闯关考核为长留",
            "subtitle": "闯关考核为长留",
            "url": "http://www.iqiyi.com/v_19rrohjid8.html"
        },
        {
            "name": "_0004_花千骨未删减版第4集_如愿以偿入长留__不可说",
            "no": "第4集_如愿以偿入长留",
            "subtitle": "如愿以偿入长留",
            "url": "http://www.iqiyi.com/v_19rrohjjlw.html"
        },
        {
            "name": "_0005_花千骨未删减版第5集_杖刑五十入仙牢__不可说",
            "no": "第5集_杖刑五十入仙牢",
            "subtitle": "杖刑五十入仙牢",
            "url": "http://www.iqiyi.com/v_19rroh1wm4.html"
        },
        {
            "name": "_0006_花千骨未删减版第6集_接任掌门遭质疑__不可说",
            "no": "第6集_接任掌门遭质疑",
            "subtitle": "接任掌门遭质疑",
            "url": "http://www.iqiyi.com/v_19rroh1iyk.html"
        },
        {
            "name": "_0007_花千骨未删减版第7集_骨头圣君初相识__不可说",
            "no": "第7集_骨头圣君初相识",
            "subtitle": "骨头圣君初相识",
            "url": "http://www.iqiyi.com/v_19rroh1ly8.html"
        },
        {
            "name": "_0008_花千骨未删减版第8集_怒接三掌得人心__不可说",
            "no": "第8集_怒接三掌得人心",
            "subtitle": "怒接三掌得人心",
            "url": "http://www.iqiyi.com/v_19rrohaz2w.html"
        },
        {
            "name": "_0009_花千骨未删减版第9集_大事办妥回长留__不可说",
            "no": "第9集_大事办妥回长留",
            "subtitle": "大事办妥回长留",
            "url": "http://www.iqiyi.com/v_19rrohayxc.html"
        },
        {
            "name": "_0010_花千骨未删减版第10集_仙剑大会拼命一搏__不可说",
            "no": "第10集_仙剑大会拼命一搏",
            "subtitle": "仙剑大会拼命一搏",
            "url": "http://www.iqiyi.com/v_19rrofiulc.html"
        },
        {
            "name": "_0011_花千骨未删减版第11集_白子画收花千骨为徒__不可说",
            "no": "第11集_白子画收花千骨为徒",
            "subtitle": "白子画收花千骨为徒",
            "url": "http://www.iqiyi.com/v_19rrofix1s.html"
        },
        {
            "name": "_0012_花千骨未删减版第12集_画骨甜蜜同居伊始__不可说",
            "no": "第12集_画骨甜蜜同居伊始",
            "subtitle": "画骨甜蜜同居伊始",
            "url": "http://www.iqiyi.com/v_19rrofnscw.html"
        },
        {
            "name": "_0013_花千骨未删减版第13集_Undefined_Attribute__不可说",
            "no": "第13集_Undefined Attribute",
            "subtitle": "Undefined Attribute",
            "url": "http://www.iqiyi.com/v_19rrofnrls.html"
        },
        {
            "name": "_0014_花千骨未删减版第14集_花千骨下山历练__不可说",
            "no": "第14集_花千骨下山历练",
            "subtitle": "花千骨下山历练",
            "url": "http://www.iqiyi.com/v_19rrof5yko.html"
        },
        {
            "name": "_0015_花千骨未删减版第15集_小骨下山陷入三角恋__不可说",
            "no": "第15集_小骨下山陷入三角恋",
            "subtitle": "小骨下山陷入三角恋",
            "url": "http://www.iqiyi.com/v_19rroffsaw.html"
        },
        {
            "name": "_0016_花千骨未删减版第16集_白子画对决杀阡陌__不可说",
            "no": "第16集_白子画对决杀阡陌",
            "subtitle": "白子画对决杀阡陌",
            "url": "http://www.iqiyi.com/v_19rroffko0.html"
        },
        {
            "name": "_0017_花千骨未删减版第17集_紫薰花千骨斗香__不可说",
            "no": "第17集_紫薰花千骨斗香",
            "subtitle": "紫薰花千骨斗香",
            "url": "http://www.iqiyi.com/v_19rrooq7fk.html"
        },
        {
            "name": "_0018_花千骨未删减版第18集_花千骨对师尊动情__不可说",
            "no": "第18集_花千骨对师尊动情",
            "subtitle": "花千骨对师尊动情",
            "url": "http://www.iqiyi.com/v_19rrooqago.html"
        },
        {
            "name": "_0019_花千骨未删减版第19集_东方彧卿性命垂危__不可说",
            "no": "第19集_东方彧卿性命垂危",
            "subtitle": "东方彧卿性命垂危",
            "url": "http://www.iqiyi.com/v_19rronng40.html"
        },
        {
            "name": "_0020_花千骨未删减版第20集预告_Undefined_Attribute__不可说",
            "no": "第20集预告_Undefined Attribute",
            "subtitle": "Undefined Attribute",
            "url": "http://www.iqiyi.com/v_19rrookxwg.html"
        },
        {
            "name": "_0021_花千骨未删减版第21集预告_Undefined_Attribute__不可说",
            "no": "第21集预告_Undefined Attribute",
            "subtitle": "Undefined Attribute",
            "url": "http://www.iqiyi.com/v_19rronmy0s.html"
        }
    ],
    "more": false,
    "title": "花千骨未删减版_不可说",
    "total": 21,
    "type": "list"
}
>>> 
```

*单视频解析* 测试

```
>>> v = run.Parse('http://www.iqiyi.com/v_19rrooq7fk.html')
>>> p(v)
{
    "data": [
        {
            "ext": "flv",
            "label": "4_1080p_1920x1080_flv_45:03.402_8",
            "size": "971.15 MB"
        },
        {
            "ext": "flv",
            "label": "2_720p_1280x720_flv_45:03.402_8",
            "size": "496.04 MB"
        },
        {
            "ext": "flv",
            "label": "0_普清_896x504_flv_45:03.402_8",
            "size": "199.60 MB"
        },
        {
            "ext": "flv",
            "label": "-1_低清_640x360_flv_45:03.402_8",
            "size": "135.75 MB"
        },
        {
            "ext": "flv",
            "label": "-3_渣清_384x216_flv_45:03.800_8",
            "size": "70.65 MB"
        }
    ],
    "name": "_0017_花千骨未删减版第17集_紫薰花千骨斗香__不可说",
    "type": "formats"
}
>>> 
```

### 3.4 测试 `ParseURL()`

```
>>> v2 = json.loads(v)
>>> l = v2['data'][0]['label']
>>> l
'4_1080p_1920x1080_flv_45:03.402_8'
>>> u = 'http://www.iqiyi.com/v_19rrooq7fk.html'
>>> info = run.ParseURL(u, l)
>>> p(info)
[
    {
        "args": {},
        "protocol": "http",
        "value": "http://163.177.114.1/videos/v0/20150705/a2/35/8f32f3fb23ca110c7bf35b328677bd20.f4v?key=0f5b98f29ab00f806ab55a3d570ee6522&src=iqiyi.com&ran=1642&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-47"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://119.188.173.11/videos/v0/20150705/a2/35/508dab90161aaeb0bdbdc733f2f5485c.f4v?key=0d6b6428888373b56ab55a3d570ee6522&src=iqiyi.com&ran=1800&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-46"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://119.188.173.18/videos/v0/20150705/a2/35/4c52535cfabdd9b672d842b15e21744d.f4v?key=09777111a13989ca2ab55a3d570ee6522&src=iqiyi.com&ran=1145&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-45"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://163.177.114.23/videos/v0/20150705/a2/35/20a6911c48b3231a924bd99b05856e6d.f4v?key=0811c9984e16de7caab55a3d570ee6522&src=iqiyi.com&ran=1267&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-47"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://163.177.114.32/videos/v0/20150705/a2/35/6eb480d8f6dafc7fe843699a46d07c83.f4v?key=0b31357ce1fefe19bab55a3d570ee6522&src=iqiyi.com&ran=1461&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-46"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://119.188.173.15/videos/v0/20150705/a2/35/5228849a32dd7bfebc62c6cca6de62cb.f4v?key=0eb984e05e06e5539ab55a3d570ee6522&src=iqiyi.com&ran=1245&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-45"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://119.188.173.22/videos/v0/20150705/a2/35/b2a2c01257d449b94e6f1a530fa44fd6.f4v?key=09d2c862cca51174fab55a3d570ee6522&src=iqiyi.com&ran=1665&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-47"
    },
    {
        "args": {},
        "protocol": "http",
        "value": "http://119.188.173.17/videos/v0/20150705/a2/35/d4cd587db85fbfef7b9847f4fd496d98.f4v?key=0608854087ff8df8eab55a3d570ee6522&src=iqiyi.com&ran=1149&qyid=0075643fbbcae57319025f514e2206ee&qypid=378337100_11&retry=1&uuid=b678d5b1-55a21136-46"
    }
]
>>> 
```


:: end lieying_plugin.md, <https://github.com/sceext2/lieying_plugin>


