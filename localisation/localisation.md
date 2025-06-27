# 本地化
游戏内支持的本地化语言共有以下几种：
>- l_english
>- l_simp_chinese
>- l_french
>- l_german
>- l_spanish
>- l_braz_por
>- l_polish
>- l_russian
>- l_japanese
## 格式
### 文件夹结构格式
本地化文件位于`localisation`中**依据语言进行分类**的（例如`simp_chinese`）文件夹中。<br>
这些文件夹也可建立新的文件夹以进一步细分。
### 文件格式
本地化文件遵循以下格式：
>- 本地化文件扩展名储存为`.yml`。
>- 文件命名末尾应包含本地化语言名称（如`l_simp_chinese`）。
>- 文件编码必须为`UTF-8 with BOM`。
### 内容格式
#### 基础本地化内容格式
以下为一个基础本地化文件示例：
```
l_simp_chinese:  
 library:0 "图书馆"
```
其中，`l_simp_chinese:`以语言名称作为文件开头；`library`是本地化键值；`0`是本地化版本号（可选）；`图书馆`是本地化内容。
#### 本地化内容着色
着色内容以符号`§`开头，后面跟字母或数字；`§!`标记着色内容结束。<br>
以下为一个本地化示例：
```
l_simp_chinese:
 angry: "§R红温§!"
```
其中，本地化输出时`红温`这部分本地化内容将被着色为红色。
>*tips：使用IDEA时可选中本地化文本，再点击上方色块进行着色。同时本地化预览时同样可渲染上色文本*

关于本地化着色的更多信息，可参考[Wiki](https://hoi4.paradoxwikis.com/Localisation#Colouring_characters "点击跳转至页面")。
#### 本地化内容嵌入图片
图片嵌入内容以符号`£`进行插入。
以下为一个本地化示例：
```
l_simp_chinese:
 happy: "高兴£GFX_happy_face£"
```
其中，将会读取名为`GFX_happy_face`的图像在并在本地化内容中插入。