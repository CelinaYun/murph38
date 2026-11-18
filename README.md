# 汉米尔顿 墨菲 38 · 星尘蓝盘（粉丝致敬项目）

一个单文件的「网络对时 + 世界时区 + 星际穿越彩蛋」页面。深色 HUD 风格，**全站中文**，界面为 iOS「液态玻璃（Liquid Glass）」质感：半透明磨砂、镜面高光、内阴影，所有方块组件均为胶囊或大圆角。

## 文件

| 文件 | 说明 |
|---|---|
| `hamilton-murph-38-blue-steel.html` | 主交付物，单文件、无任何外部依赖（表盘/指针/图标全部内嵌 base64） |
| `hamilton-murph-38-ios.html` | iOS / PWA 版本（追加 apple 全屏 meta、启动图、Service Worker） |
| `manifest.webmanifest` | PWA 清单（图标内嵌） |
| `deploy/murph38-ios-pwa.zip` | 可直接拖到 Netlify Drop / Sites→Deploys 的部署包（含 `_headers`） |
| `deploy/murph38/dial.webp` | 透明底表盘图（640px），供 Scriptable 小组件使用 |
| `murph38-scriptable-widget.js` | iOS 桌面小组件脚本（Scriptable，小号/中号） |
| `scripts/build_ios.py` | 由主文件生成 iOS/PWA 版 |
| `scripts/build_deploy.py` | 生成部署目录、`_headers` 与 zip |

## 功能

- **NTP 对时**：以 `ntp.ntsc.ac.cn`（国家授时中心）为基准，在线复核走 授时中心 → timeapi → worldtimeapi 三级降级；失败时使用构建校准值并明确标注
- **世界时区**：20 个城市，点击切换，时针/分针用欠阻尼弹簧摆动到位，秒针全球同步
- **走时模拟**：机械 6Hz（H-10 步频）/ 石英 1Hz / 平滑扫描 三种模式
- **夜光模式**：Super-LumiNova 绿
- **彩蛋**：点击「EUREKA 彩蛋」或地图上的卡冈图雅星标 → 全屏五维超立方体，提线木偶库珀拨动书脊传引力方程，秒针以摩尔斯电码拍出 E U R E K A；场景内右上角小手表与主表秒针严格同步
- **表盘模式**：`?face` 只保留全屏表盘，适合「添加到主屏幕」当桌面图标

## 本地使用

直接用浏览器打开 `hamilton-murph-38-blue-steel.html` 即可，无构建、无依赖。

在线版：

- GitHub Pages：<https://celinayun.github.io/murph38/>
- 表盘模式（可添加到主屏幕）：<https://celinayun.github.io/murph38/?face>
- Netlify 镜像：<https://murphy-watch.netlify.app>

## 构建（可选）

```bash
python scripts/build_ios.py      # 生成 hamilton-murph-38-ios.html + manifest
python scripts/build_deploy.py   # 生成 deploy/murph38/ 与 zip
```

## 说明

- 粉丝致敬作品，与 Hamilton Watch、派拉蒙/传奇影业无关；表盘照片仅作个人非商业用途
- 页面文案全部为中文；保留的非中文项均为标识符：`EUREKA`（摩尔斯电码内容）、`Asia/Shanghai`、`UTC+8`、`ntp.ntsc.ac.cn`、`6Hz / 1Hz`、`H-10`
