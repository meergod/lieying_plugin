:: lieying_plugin_test.md, language *Chinese* (`zh_cn`)
:: *last_update* `2015-07-27 12:10 GMT+0800 CST`

# 猎影插件接口 示例

+ 此 示例, 适用于 
  [猎影插件接口](https://github.com/sceext2/lieying_plugin/blob/master/doc/lieying_plugin.md) 
  version 0.2.1 

**注意**: 
由于 `0.3.0` 版本的 *猎影插件接口*, 还没有 相应的 *猎影插件*, 
所以 以下 测试 示例, 仍然使用 `0.2.1` 版本的 *猎影插件接口*. 


## 内容目录

+ **[0. 导入插件 其他初始化工作](#0-导入插件-其他初始化工作)**

+ **[1. 测试 `GetVersion()`](#1-测试-getversion)**

+ **[2. 测试 `Parse()`](#2-测试-parse)**
  
  + **[2.1 *多视频解析* 测试](#21-多视频解析-测试)**
  + **[2.2 *单视频解析* 测试](#22-单视频解析-测试)**

+ **[3. 测试 `ParseURL()`](#3-测试-parseurl)**


## 0. 导入插件, 其他初始化工作

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


## 1. 测试 `GetVersion()`

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


## 2. 测试 `Parse()`

### 2.1 *多视频解析* 测试

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

### 2.2 *单视频解析* 测试

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


## 3. 测试 `ParseURL()`

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


:: end lieying_plugin_test.md, <https://github.com/sceext2/lieying_plugin>


