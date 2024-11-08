# AutoLoginJXNUwifi_bycursorAI

⚠️ **注意：这是一个由 Cursor AI 100% 自动生成的项目，目前功能仍在开发中，可能无法正常使用。**

江西师范大学校园网自动登录工具

## 项目说明

本项目基于以下开源项目的思路
- [@huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)
- [@realZnS/jxnu-srun-go](https://github.com/realZnS/jxnu-srun-go)
- [JXNU校园网登录的实现](https://blog.csdn.net/qq_41797946/article/details/89417722)

## 功能特点

- 图形化界面，简单易用
- 自动检测并连接JXNU校园网
- 支持保存账号信息（可选）
- 支持开机自动登录（可选）
- 支持连接校园网时自动登录（可选）
- 支持移动、联通和电信运营商选择
- 系统托盘运行，不干扰正常使用
- 支持显示/隐藏密码功能

## 使用说明

1. 下载并运行程序
2. 输入校园网账号和密码
3. 选择运营商
4. 选择自动登录选项：
   - 开机自动登录：开机时自动运行程序
   - 连接校园网时自动登录：检测到连接jxnu_stu时自动登录
5. 点击"保存配置"保存设置
6. 点击"登录"测试连接

## 注意事项

- 本程序仅供学习交流使用
- 请勿将账号密码分享给他人
- 程序会在系统托盘运行，可随时打开主界面修改设置
- 可以通过托盘菜单完全退出程序
- ⚠️ 当前版本可能存在功能问题，仍在开发中

## 技术实现

- 使用Python 3.8+
- GUI基于PyQt6实现
- 网络请求使用requests库
- 自动打包使用pyinstaller
- 支持Windows系统

## 开发状态

⚠️ **当前状态：开发中**
- 登录功能可能不稳定
- 注销功能尚未完善
- 自动重连功能需要优化
- 欢迎提交Issue和PR帮助改进

## 免责声明

- 本项目完全由 Cursor AI 生成，可能存在功能缺陷
- 代码逻辑基于上述开源项目的思路
- 仅供学习研究使用，请勿用于违反校规的行为
- 使用本程序产生的任何问题由使用者自行承担

## 致谢

感谢以下项目提供的思路和参考：
- [@huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)
- [@realZnS/jxnu-srun-go](https://github.com/realZnS/jxnu-srun-go)
- [JXNU校园网登录的实现](https://blog.csdn.net/qq_41797946/article/details/89417722)
