---
title: 轻雪函数
icon: code
order: 4
category: 使用指南
tag:
  - 配置
---

## **轻雪函数**

轻雪函数 Liteyuki Function 是轻雪的一个功能，它允许你在轻雪中运行一些自定义的由数据驱动的命令，类似于Minecraft的mcfunction

### **函数文件**

函数文件放在资源包的`functions`目录下，文件名以`.mcfunction` `.lyfunction` `.lyf`结尾，例如`test.mcfunction`，文件内容为一系列的命令，每行一个命令，支持单行注释`#`，例如：

```shell
cmd echo hello
```

### **命令文档**

```shell
var <var1=value1> [var2=value2] ...  # 定义变量
cmd <command>  # 在设备上执行命令
api <api_name> [var=value...]  # 调用Bot API
function <func_name> # 调用函数，可递归
sleep <time>  # 异步等待，单位s
nohup <command>  # 使用新的task执行命令，即不等待
end # 结束函数关键字，包括子task
await # 等待所有异步任务结束，若函数中启动了其他task，需要在最后调用，否则task对象会被销毁
```


### **示例**

```shell
# 疯狂戳好友
# 使用 /function poke user_id=123456 执行
# 每隔0.2s戳两次，无限戳，会触发最大递归深度限制
# 若要戳20s后停止，则需要删除await，添加sleep 20和end
api friend_poke user_id=user_id
api friend_poke user_id=user_id
sleep 0.2
nohup function poke
await
```