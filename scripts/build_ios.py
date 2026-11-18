#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build iOS PWA variant of the Hamilton Murph 38 clock page."""
import os, shutil

BASE = 'C:/Users/Administrator/WorkBuddy/2026-10-20-16-38-05'
TMP = BASE + '/.workbuddy/tmp'

src = open(BASE + '/hamilton-murph-38-blue-steel.html', encoding='utf-8').read()
b64_180 = open(TMP + '/icon_180_b64.txt').read()
b64_sp390 = open(TMP + '/splash390_b64.txt').read()
b64_sp393 = open(TMP + '/splash393_b64.txt').read()
b64_sp1284 = open(TMP + '/splash1284_b64.txt').read()

inject = (
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    '<meta name="apple-mobile-web-app-title" content="墨菲38">\n'
    '<meta name="application-name" content="墨菲38">\n'
    '<meta name="theme-color" content="#0b1220">\n'
    '<meta name="format-detection" content="telephone=no">\n'
    '<link rel="apple-touch-icon" href="data:image/png;base64,' + b64_180 + '">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="apple-touch-startup-image" media="(device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3)" href="data:image/png;base64,' + b64_sp390 + '">\n'
    '<link rel="apple-touch-startup-image" media="(device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3)" href="data:image/png;base64,' + b64_sp393 + '">\n'
    '<link rel="apple-touch-startup-image" media="(device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3)" href="data:image/png;base64,' + b64_sp1284 + '">\n'
    '<link rel="apple-touch-startup-image" href="data:image/png;base64,' + b64_sp390 + '">\n'
)

old_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
new_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">'
out = src.replace(old_viewport, new_viewport + '\n' + inject, 1)
assert new_viewport in out

extra = r"""
<script>
(function(){
  /* 防 iOS 双击缩放 / 长按菜单 */
  document.addEventListener('gesturestart', function(e){ e.preventDefault(); });
  document.addEventListener('dblclick', function(e){ e.preventDefault(); }, {passive:false});
  var lastTouch = 0;
  document.addEventListener('touchend', function(e){
    var now = Date.now();
    if (now - lastTouch <= 300) e.preventDefault();
    lastTouch = now;
  }, {passive:false});

  /* 全屏安全区适配（iOS 刘海/底部横条） */
  var st = document.createElement('style');
  st.textContent = [
    '@supports (padding: max(0px)) {',
    '  body {',
    '    padding-left: max(18px, env(safe-area-inset-left));',
    '    padding-right: max(18px, env(safe-area-inset-right));',
    '    padding-bottom: max(60px, env(safe-area-inset-bottom));',
    '  }',
    '}',
    'html { -webkit-text-size-adjust: 100%; }',
    'body {',
    '  -webkit-user-select: none; user-select: none;',
    '  -webkit-touch-callout: none;',
    '  -webkit-tap-highlight-color: transparent;',
    '}'
  ].join('\n');
  document.head.appendChild(st);

  /* Service Worker：使 PWA 可离线打开 */
  if ('serviceWorker' in navigator) {
    var swCode = [
      "const CACHE = 'murph38-v2-map';",
      "const PAGE = './hamilton-murph-38-ios.html';",
      "self.addEventListener('install', e => {",
      "  e.waitUntil(caches.open(CACHE).then(c => c.addAll(['./hamilton-murph-38-ios.html', './manifest.webmanifest'])).then(() => self.skipWaiting()));",
      "});",
      "self.addEventListener('activate', e => { e.waitUntil(self.clients.claim()); });",
      "self.addEventListener('fetch', e => {",
      "  if (e.request.method !== 'GET') return;",
      "  e.respondWith(",
      "    caches.match(e.request).then(r => r || fetch(e.request).then(res => {",
      "      const copy = res.clone();",
      "      caches.open(CACHE).then(c => c.put(e.request, copy));",
      "      return res;",
      "    }).catch(() => caches.match(PAGE)))",
      "  );",
      "});"
    ].join('\n');
    var blob = new Blob([swCode], {type: 'text/javascript'});
    var swUrl = URL.createObjectURL(blob);
    navigator.serviceWorker.register(swUrl).catch(function(){ /* file:// 下自动忽略 */ });
  }
})();
</script>
"""

out = out.replace('</body>', extra + '</body>', 1)

dst = BASE + '/hamilton-murph-38-ios.html'
open(dst, 'w', encoding='utf-8').write(out)
shutil.copy(TMP + '/manifest.webmanifest', BASE + '/manifest.webmanifest')

print('written', dst, os.path.getsize(dst))
print('written', BASE + '/manifest.webmanifest', os.path.getsize(BASE + '/manifest.webmanifest'))
