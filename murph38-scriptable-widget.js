// ============================================================
// 墨菲 38 · iOS 桌面小组件（Scriptable）
// ------------------------------------------------------------
// 用法：
//   1. App Store 装「Scriptable」（免费）
//   2. 打开 Scriptable → 右上 + → 粘贴本文件全部内容 → 命名「墨菲38」
//   3. 回到主屏幕长按 → 左上 + → 搜索 Scriptable → 选小号/中号
//   4. 长按刚加的组件 → 编辑小组件 → Script 选「墨菲38」
// ------------------------------------------------------------
// 说明：
//   · 表盘图片来自 https://celinayun.github.io/murph38/dial.webp（首次加载后本地缓存）
//   · iOS 不允许小组件逐秒刷新，系统大约 15 分钟给一次机会；
//     所以秒针停在「生成这一刻」的位置，分针/时针始终准确。
//   · 想换时区，改下面的 TZ 常量（Asia/Shanghai / America/New_York ...）
// ============================================================

const DIAL_URL = "https://celinayun.github.io/murph38/dial.webp"
const TZ = "Asia/Shanghai"
const BG_HEX = "#05080f"
const CREAM = new Color("#e8dcc0")
const ICE = new Color("#8fd0ff")

// ---------- 取表盘图（带缓存） ----------
async function loadDial() {
  const fm = FileManager.local()
  const path = fm.joinPath(fm.cacheDirectory(), "murph38-dial.webp")
  if (fm.fileExists(path)) {
    const cached = fm.readImage(path)
    if (cached) return cached
  }
  const img = await new Request(DIAL_URL).loadImage()
  if (img) fm.writeImage(path, img)
  return img
}

// ---------- 画一根指针（用多边形，避免旋转 API） ----------
function drawHand(dc, cx, cy, deg, len, tail, width, color) {
  const a = (deg * Math.PI) / 180
  const dx = Math.sin(a), dy = -Math.cos(a)      // 指向
  const px = Math.cos(a), py = Math.sin(a)       // 垂直
  const hw = width / 2
  const tipX = cx + dx * len, tipY = cy + dy * len
  const backX = cx - dx * tail, backY = cy - dy * tail

  const p = new Path()
  p.move(new Point(tipX + px * hw, tipY + py * hw))
  p.addLine(new Point(tipX - px * hw, tipY - py * hw))
  p.addLine(new Point(backX - px * hw, backY - py * hw))
  p.addLine(new Point(backX + px * hw, backY + py * hw))
  p.closeSubpath()

  dc.addPath(p)
  dc.setFillColor(color)
  dc.fillPath()
}

// ---------- 组装表盘（图片 + 三根针） ----------
async function buildDial(baseSize) {
  const img = await loadDial()
  const dc = new DrawContext()
  dc.size = new Size(baseSize, baseSize)
  dc.opaque = false
  dc.respectScreenScale = true

  if (img) dc.drawImageInRect(img, new Rect(0, 0, baseSize, baseSize))

  const now = new Date()
  // 目标时区的小时/分钟/秒
  const fmt = new DateFormatter()
  fmt.dateFormat = "H:mm:ss"
  fmt.locale = "en_US"
  fmt.timeZone = TZ
  const parts = fmt.string(now).split(":").map(function (v) { return parseInt(v, 10) })
  const h = parts[0] % 12, m = parts[1], s = parts[2]

  const cx = baseSize / 2, cy = baseSize / 2
  drawHand(dc, cx, cy, (h + m / 60) * 30, baseSize * 0.26, baseSize * 0.05, baseSize * 0.042, CREAM)
  drawHand(dc, cx, cy, (m + s / 60) * 6, baseSize * 0.38, baseSize * 0.06, baseSize * 0.030, CREAM)
  drawHand(dc, cx, cy, s * 6, baseSize * 0.42, baseSize * 0.10, baseSize * 0.013, ICE)

  dc.setFillColor(ICE)
  dc.fillEllipse(new Rect(cx - baseSize * 0.016, cy - baseSize * 0.016, baseSize * 0.032, baseSize * 0.032))

  return dc.getImage()
}

// ---------- 组件本体 ----------
const family = config.widgetFamily || "medium"
const widget = new ListWidget()
widget.backgroundColor = new Color(BG_HEX)
widget.setPadding(8, 8, 8, 8)

const now = new Date()
const clockFmt = new DateFormatter()
clockFmt.dateFormat = "HH:mm"
clockFmt.timeZone = TZ
const dateFmt = new DateFormatter()
dateFmt.dateFormat = "M月d日 EEEE"
dateFmt.locale = "zh_CN"
dateFmt.timeZone = TZ

if (family === "small") {
  const dial = await buildDial(300)
  const stack = widget.addStack()
  stack.addSpacer()
  const imgEl = stack.addImage(dial)
  imgEl.imageSize = new Size(132, 132)
  stack.addSpacer()
  widget.addSpacer(2)
  const t = widget.addText(clockFmt.string(now))
  t.font = Font.mediumMonospacedSystemFont(13)
  t.textColor = CREAM
  t.centerAlignText()
} else {
  const row = widget.addStack()
  row.centerAlignContent()

  const dial = await buildDial(300)
  const imgEl = row.addImage(dial)
  imgEl.imageSize = new Size(118, 118)

  row.addSpacer(10)

  const col = row.addStack()
  col.layoutVertically()
  col.addSpacer()

  const t = col.addText(clockFmt.string(now))
  t.font = Font.lightMonospacedSystemFont(30)
  t.textColor = CREAM

  const d = col.addText(dateFmt.string(now))
  d.font = Font.systemFont(10)
  d.textColor = new Color("#8fa6c0")
  d.textOpacity = 0.9

  const c = col.addText("北京 · 墨菲 38")
  c.font = Font.systemFont(9)
  c.textColor = new Color("#7d8ea6")

  col.addSpacer()
}

// 15 分钟后再刷新（iOS 会给的是「不早于」，实际可能更晚）
widget.refreshAfterDate = new Date(Date.now() + 15 * 60 * 1000)

if (config.runsInWidget) {
  Script.setWidget(widget)
} else {
  widget.presentMedium()
}
Script.complete()
