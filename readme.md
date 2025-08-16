# 欢迎加入Mod制作行列！
## 说明
本Mod为模组制作教程&模板类，请开启**debug**模式并在编辑器中**打开文件夹**以获得最佳体验。Mod中教程及提供工具仅供学习交流使用。  
教程Mod中所含文件夹基本均有说明文档及模板，工具类均存放于`tools`文件夹中。
> *tips：由于**HOIModEditor**程序的特殊性，单独从`tools`文件夹中独立出来。*
## 制作Mod前的准备工作
### 下载文本编辑器
制作mod所常用的文本编辑器有[VS code](https://code.visualstudio.com "点击前往官网")（以下简称VSC）、[PyCharm](https://www.jetbrains.com/zh-cn/pycharm "点击前往官网")（以下简称PYC）与[Notepad++](https://notepad-plus-plus.org "点击前往官网")（以下简称NP++）。

| 软件 | [VS code](https://code.visualstudio.com "点击前往官网") | [PyCharm](https://www.jetbrains.com/zh-cn/pycharm/ "点击前往官网") | [Notepad++](https://notepad-plus-plus.org "点击前往官网") |
|:--:|:-------------------------------------------------:|:------------------------------------------------------------:|:---------------------------------------------------:|
| 优点 |                    插件较多、用户数量多                     |                  可通过嵌入提示快速了解信息，支持添加多个Mod进索引                  |                    轻量、无需插件和复杂配置                     |
| 缺点 |                    插件配置及上手难度较大                    |                      插件较少，有时语言解析会出现不明问题                      |                   功能有限，不适合大型项目开发                    |
> *tips：使用本Mod的人员建议使用 **[PyCharm](https://www.jetbrains.com/zh-cn/pycharm "点击前往官网")** 以获取最佳开发体验。*
### 安装插件
#### 对于使用VSC的人员，建议安装下列插件：
- [Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=MS-CEINTL.vscode-language-pack-zh-hans "点击前往插件页面")（VSC中文语言包）
- [CWTools - Paradox Language Services](https://marketplace.visualstudio.com/items?itemName=tboby.cwtools-vscode "点击前往插件页面")（P社语言解析工具）
- [VModer - HOI4 Language Server](https://marketplace.visualstudio.com/items?itemName=textGamex.VModer "点击前往插件页面")（CWTools扩展）
- [HOI4 Mod Utilities](https://marketplace.visualstudio.com/items?itemName=Chaofan.hoi4modutilities "点击前往插件页面")（部分界面图形化预览工具）
#### 对于使用PYC的人员，建议安装下列插件：
- [Paradox Language Support](https://plugins.jetbrains.com/plugin/16825-paradox-language-support "点击前往插件页面")（P社语言解析工具）
- [Translation](https://plugins.jetbrains.com/plugin/8579-translation "点击前往插件页面")（可与 *Paradox Language Support* 插件联动提供一些[额外功能](https://windea.icu/Paradox-Language-Support/zh/plugin-integration.md "点击前往说明文档页面")）
## 创建Mod
### 对于HOIModEditor：
1. 单击左侧**Mod创建**
2. 按照提示输入的Mod的各项信息
3. 完成后单击**开始创建**按钮，一个空白Mod便创建完毕。
### 对于官方启动器：
1. 打开启动器，单击左侧**Mod 库**。
2. 单击**上传 MOD**按钮，点击**创建 MOD**。
3. **名称**处输入Mod名称，**版本**处输入Mod版本号，**路径**处输入想让Mod所处文件夹名称，**标签**处勾选符合Mod的标签。
4. 完成后单击**创建 MOD**按钮，一个空白Mod便创建完毕。
## 打开Mod项目
新创建的Mod文件夹保存于路径`%userprofile%\Documents\Paradox Interactive\Hearts of Iron IV\mod`中，Mod文件夹名称为此前输入的路径。  
使用VSC或PYC打开文件夹，并在插件中设置游戏本体文件夹路径。  
### 对于VSC：
1. 点击左下角，打开**设置**，点击**扩展**。
2. 找到**钢四模组工具**，在**Install Path**一栏输入游戏文件夹路径，在**Mod File**一栏输入模组定义文件（即 `descriptor.mod` 文件）路径。
3. 找到**CWTools Configuration**，在**Cwtools > Cache: Hoi4**一栏输入游戏文件夹路径。
4. 找到**VModer Configuration**，在**Game Root Path**一栏输入游戏文件夹路径。
### 对于PYC：
1. 按下快捷键**Ctrl+Alt+M**，在**游戏目录**一栏输入游戏本地文件夹路径，或点击**快速选择游戏目录**自动寻找。
2. 在**模组依赖**一栏添加其他Mod（可选，通常用于制作附属Mod时使用）。

等待索引完成，即可开始制作Mod。
## Mod结构
### descriptor.mod文件
descriptor.mod文件即模组定义文件，其中包含有Mod的各种信息。详细内容参考 `descriptor.md` 文件。
### thumbnail.png/thumbnail.gif文件
Mod封面文件，同时也是上传至Steam创意工坊的封面文件。
### 文件夹
Mod文件夹结构与原版游戏基本相同，关于原版文件夹内容可参考本Mod中`documentation\folder.html`文件或[此页面](https://docs.szlib.eu/zh/%E4%BB%A3%E7%A0%81/%E6%B8%B8%E6%88%8F%E6%96%87%E4%BB%B6%E6%9E%B6%E6%9E%84 "点击前往页面")。
## Mod读取
Mod中文件读取遵从下列条件：
- 当Mod文件与游戏本体文件不重复时，同时读取。
- 当Mod中部分文件与游戏本体文件重复，优先读取Mod中的文件。
- 当读取至`descriptor.mod`文件中`replace_path`的文件夹时，跳过游戏本体中次文件夹，直接读取Mod中此文件夹。
- 当子Mod与主Mod文件重复时，优先读取子Mod中的文件。
## Debug模式
debug模式是为了便于对游戏内数据进行各项测试的模式，可通过下列方式开启：
### Steam端开启
1. 在Steam库中找到钢四，右键单击**属性**。
2. 在**通用**中找到高级启动选项，输入`-debug`。
### 本地端开启
1. 找到游戏根目录，为`dowser.exe`文件创建一个快捷方式。
2. 右键单击快捷方式，打开**属性**。
3. 在**目标**路径后面添加` -debug`。
> *tips:注意此处是``" -debug"``而非`-debug`，**短横前方有空格！***

debug模式与正常模式略有区别：
- 游戏主界面加载完成后将会自动使用记事本弹出`error.log`文件。
- 在主界面按下`~`键将会显示gui边框，游戏中需通过控制台输入`gui`来打开。
- 显示gui边框时按住`Ctrl+Alt+鼠标右键`可以对gui进行**打开文件**、**查看路径**以及**刷新**操作。
- 本地化等修改可热更新（新建文件除外）。
- 多人模式将**禁用**。
## 日志
日志文件位于`%userprofile%\Documents\Paradox Interactive\Hearts of Iron IV\logs`中，其中`error.log`与`game.log`两个文件最为常用。<br>
通常情况下，当游戏出现错误时，错误信息会被记录在`error.log`文件中；`game.log`一般记录的是游戏运行时的日志（如`log = xx`此类效果的记录）。<br>
当游戏出现严重错误甚至崩溃时，查看日志能够更有效地排查出错误原因。
>*tips：某些错误可能在崩溃前来不及被记录，**甚至根本不会被记录**。*
