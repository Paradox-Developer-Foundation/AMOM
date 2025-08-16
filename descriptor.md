# descriptor.mod文件
`descriptor.mod`文件中包含有Mod的各种信息，在创建Mod后自动创建，以下是一个示例：
```paradox_script
version = "0.0.0"
tags = {
	"Alternative History"
}
name = "test"
supported_version = "1.16.*"
replace_path = common/bookmarks
picture = thumbnail.png
```
其中各部分内容如下：
- `version = xxx` Mod版本。
- `name = xxx` Mod名称。
- `tags = { xxx }` 包含创建Mod时勾选的标签。
- `picture = "thumbnail.png"` Mod封面。
- `replace_path = xxx` 包含Mod将要替换的文件夹。
- `supported_version = *.*.*` Mod所支持的游戏版本
- `remote_file_id = *` Mod在Steam创意工坊上的id，**上传之后自动生成，无需手动添加分配**。