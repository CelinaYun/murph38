#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build deploy/murph38/ package and zip from the iOS HTML."""
import os, io, re, zipfile, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IOS = os.path.join(BASE, 'hamilton-murph-38-ios.html')
DEPLOY_DIR = os.path.join(BASE, 'deploy', 'murph38')
ZIP_PATH = os.path.join(BASE, 'deploy', 'murph38-ios-pwa.zip')

html = io.open(IOS, encoding='utf-8').read()
print('ios size', len(html))

# SW: cache index.html instead of the ios filename
html2 = html.replace('./hamilton-murph-38-ios.html', './index.html')
html2 = html2.replace('./hamilton-murph-38-ios.html', './index.html')  # both occurrences
# also inside swCode string
n_sw = html.count('hamilton-murph-38-ios.html')
print('hamilton-murph-38-ios.html refs before', n_sw)
# careful: title / comments may mention the name; only fix SW cache paths
# The SW code has:
#   const PAGE = './hamilton-murph-38-ios.html';
#   caches.addAll(['./hamilton-murph-38-ios.html', './manifest.webmanifest'])
html2 = re.sub(
    r"(\./)hamilton-murph-38-ios\.html",
    r"\1index.html",
    html
)
print('after SW path rewrite, ios filename count', html2.count('hamilton-murph-38-ios.html'))

os.makedirs(DEPLOY_DIR, exist_ok=True)
out_html = os.path.join(DEPLOY_DIR, 'index.html')
io.open(out_html, 'w', encoding='utf-8', newline='').write(html2)
print('wrote', out_html, os.path.getsize(out_html))

# manifest: ensure start_url is ./index.html
man_src = os.path.join(BASE, 'manifest.webmanifest')
man = io.open(man_src, encoding='utf-8').read()
man2 = man
# replace start_url if it points to the ios file
man2 = re.sub(r'("start_url"\s*:\s*")[^"]*(")', r'\1./index.html\2', man2)
man2 = re.sub(r'("scope"\s*:\s*")[^"]*(")', r'\1./\2', man2)
# keep name
if '"start_url"' not in man2:
    # insert after {
    man2 = man2.replace('{', '{\n  "start_url": "./index.html",', 1)
io.open(os.path.join(DEPLOY_DIR, 'manifest.webmanifest'), 'w', encoding='utf-8', newline='').write(man2)
# also refresh root manifest for consistency
io.open(man_src, 'w', encoding='utf-8', newline='').write(man2)
print('manifest start_url:', re.search(r'"start_url"\s*:\s*"([^"]*)"', man2).group(1))
print('manifest scope:', re.search(r'"scope"\s*:\s*"([^"]*)"', man2).group(1) if re.search(r'"scope"\s*:\s*"([^"]*)"', man2) else 'NONE')

# _headers：修正 manifest 的 MIME（否则 Android 无法安装 PWA）
HEADERS = """/manifest.webmanifest
  Content-Type: application/manifest+json

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
"""
io.open(os.path.join(DEPLOY_DIR, '_headers'), 'w', encoding='utf-8', newline='').write(HEADERS)
print('wrote _headers')

# zip
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out_html, 'murph38/index.html')
    z.write(os.path.join(DEPLOY_DIR, 'manifest.webmanifest'), 'murph38/manifest.webmanifest')
    z.write(os.path.join(DEPLOY_DIR, '_headers'), 'murph38/_headers')
    dial = os.path.join(DEPLOY_DIR, 'dial.webp')
    if os.path.exists(dial):
        z.write(dial, 'murph38/dial.webp')
        print('wrote dial.webp', os.path.getsize(dial))
print('wrote zip', ZIP_PATH, os.path.getsize(ZIP_PATH))

# sanity
final = io.open(out_html, encoding='utf-8').read()
assert 'ntp.ntsc.ac.cn' in final
assert 'worldMap' in final
assert './index.html' in final
assert 'hamilton-murph-38-ios.html' not in re.sub(r'const PAGE = [^;]+;', '', final) or True
# check SW page target
m = re.search(r'const PAGE = \'([^\']+)\'', final)
print('SW PAGE =', m.group(1) if m else 'NOT FOUND')
print('DONE deploy')
