import http.server, socketserver, json, os, zipfile, re

# 1. 寻找 9结构综合97.goodnotes 并复原出完整原始附件序列
gn_files = [f for f in os.listdir('.') if f.endswith('.goodnotes')]
jg_gn = next((f for f in gn_files if "结构综合" in f), None)
if not jg_gn:
    for p in ["..", os.path.expanduser("~/Desktop/cards"), os.path.expanduser("~/Desktop/allin")]:
        cand = os.path.join(p, "9结构综合97.goodnotes")
        if os.path.exists(cand):
            jg_gn = cand
            break

if not jg_gn:
    print("❌ 未找到 9结构综合97.goodnotes 文件！")
    exit(1)

uuid_pattern = re.compile(rb'[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}')
raw_atts = []
with zipfile.ZipFile(jg_gn, 'r') as z:
    file_list = z.namelist()
    pb_data = z.read("index.events.pb") if "index.events.pb" in file_list else None
    att_files = [f for f in file_list if f.startswith("attachments/")]
    att_map = {os.path.basename(f).upper(): f for f in att_files}
    if pb_data:
        found_uuids = [u.decode('ascii').upper() for u in uuid_pattern.findall(pb_data)]
        seen = set()
        for uid in found_uuids:
            if uid in att_map and uid not in seen:
                raw_atts.append(att_map[uid])
                seen.add(uid)
    else:
        raw_atts = att_files

# 提取所有图片到 images 目录
os.makedirs("images", exist_ok=True)
all_extracted = []
with zipfile.ZipFile(jg_gn, 'r') as z:
    for idx, att in enumerate(raw_atts):
        fname = f"jiegou_raw_{idx:03d}.jpg"
        fpath = os.path.join("images", fname)
        with open(fpath, "wb") as f_out:
            f_out.write(z.read(att))
        all_extracted.append({"idx": idx, "src": f"images/{fname}", "att": att})

# 写入可视化整理器 HTML
sorter_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>结构综合 - 可视化卡片整理器</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #f2f2f7; padding: 20px; }}
  h2 {{ text-align: center; margin-bottom: 8px; }}
  .tip {{ text-align: center; color: #666; font-size: 14px; margin-bottom: 20px; }}
  .toolbar {{ position: sticky; top: 10px; z-index: 100; display: flex; justify-content: center; gap: 16px; margin-bottom: 20px; background: rgba(255,255,255,0.9); padding: 12px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
  .btn {{ padding: 10px 20px; font-size: 15px; font-weight: 600; border: none; border-radius: 8px; cursor: pointer; }}
  .btn-save {{ background: #007aff; color: white; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; max-width: 1400px; margin: 0 auto; }}
  .card-item {{ background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; flex-direction: column; align-items: center; cursor: grab; position: relative; border: 2px solid transparent; }}
  .card-item.selected {{ border-color: #ff3b30; }}
  .tag {{ font-size: 12px; font-weight: 700; margin-bottom: 6px; padding: 2px 8px; border-radius: 6px; }}
  .tag-front {{ background: #e0f2fe; color: #0284c7; }}
  .tag-back {{ background: #fef3c7; color: #d97706; }}
  .thumb {{ width: 100%; height: 180px; object-fit: contain; background: #fafafa; border-radius: 8px; border: 1px solid #eee; }}
  .actions {{ display: flex; gap: 8px; margin-top: 8px; width: 100%; }}
  .btn-sm {{ flex: 1; padding: 4px; font-size: 12px; border: none; border-radius: 6px; cursor: pointer; }}
  .btn-del {{ background: #fee2e2; color: #ef4444; }}
  .btn-swap {{ background: #e5e5ea; color: #333; }}
</style>
</head>
<body>
  <h2>🗂 结构综合 · 可视化排序与剔除</h2>
  <div class="tip">每两张图为一组（蓝标为正面/题目，黄标为背面/答案）。点【删除】剔除多余图片，拖拽卡片调整顺序。</div>
  <div class="toolbar">
    <button class="btn btn-save" onclick="saveAndBuild()">💾 保存并生成最终网页</button>
  </div>
  <div class="grid" id="grid"></div>

<script>
let items = {json.dumps(all_extracted)};

function render() {{
  const g = document.getElementById('grid');
  g.innerHTML = '';
  items.forEach((it, i) => {{
    const isFront = (i % 2 === 0);
    const div = document.createElement('div');
    div.className = 'card-item';
    div.draggable = true;
    div.dataset.index = i;
    
    div.innerHTML = `
      <div class="tag ${{isFront ? 'tag-front' : 'tag-back'}}">
        #${{i}} · 题${{Math.floor(i/2)+1}} [${{isFront ? '正面' : '背面'}}]
      </div>
      <img class="thumb" src="${{it.src}}">
      <div class="actions">
        <button class="btn-sm btn-swap" onclick="moveUp(${{i}})">← 上移</button>
        <button class="btn-sm btn-swap" onclick="moveDown(${{i}})">下移 →</button>
        <button class="btn-sm btn-del" onclick="delItem(${{i}})">删除</button>
      </div>
    `;
    
    div.ondragstart = (e) => e.dataTransfer.setData('text/plain', i);
    div.ondragover = (e) => e.preventDefault();
    div.ondrop = (e) => {{
      e.preventDefault();
      const from = parseInt(e.dataTransfer.getData('text/plain'));
      const to = i;
      const moved = items.splice(from, 1)[0];
      items.splice(to, 0, moved);
      render();
    }};
    g.appendChild(div);
  }});
}}

function moveUp(i) {{ if(i > 0) {{ const t = items[i]; items[i] = items[i-1]; items[i-1] = t; render(); }} }}
function moveDown(i) {{ if(i < items.length - 1) {{ const t = items[i]; items[i] = items[i+1]; items[i+1] = t; render(); }} }}
function delItem(i) {{
  if(confirm('确定剔除这张图（#' + i + '）吗？删除后其后面的所有图会自动重新对齐正反面！')) {{
    items.splice(i, 1);
    render();
  }}
}}

function saveAndBuild() {{
  fetch('/save', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify(items.map(it => it.att))
  }}).then(res => res.text()).then(t => alert(t));
}}

render();
</script>
</body>
</html>"""

with open("sorter.html", "w", encoding="utf-8") as f:
    f.write(sorter_html)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            
            # 1. 更新 order_rules.json
            with open("order_rules.json", "r", encoding="utf-8") as f:
                rules = json.load(f)
            key = next((k for k in rules.keys() if "结构综合" in k), "9结构综合97")
            rules[key] = data
            with open("order_rules.json", "w", encoding="utf-8") as f:
                json.dump(rules, f, ensure_ascii=False, indent=2)
                
            # 2. 生成 final HTML
            cards = []
            for i in range(0, len(data) - 1, 2):
                cards.append({
                    "id": i // 2 + 1,
                    "front": f"images/9结构综合97_{i:03d}.jpg",
                    "back": f"images/9结构综合97_{i+1:03d}.jpg"
                })
            
            # 复制对应图片到 9结构综合97_xxx.jpg
            with zipfile.ZipFile(jg_gn, 'r') as z:
                for idx, att in enumerate(data):
                    target_name = f"9结构综合97_{idx:03d}.jpg"
                    with open(os.path.join("images", target_name), "wb") as f_img:
                        f_img.write(z.read(att))
            
            cards_json = json.dumps(cards, ensure_ascii=False)
            chapter_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>9结构综合97 - 刷题卡</title>
<style>
  :root {{ --bg: #f2f2f7; --card-bg: #fff; --text: #1c1c1e; --primary: #007aff; --danger: #ff3b30; --success: #34c759; }}
  body {{ margin: 0; padding: 16px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); display: flex; flex-direction: column; align-items: center; min-height: 90vh; user-select: none; }}
  .header {{ width: 100%; max-width: 680px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }}
  .nav-back {{ font-size: 14px; color: var(--primary); text-decoration: none; font-weight: 600; padding: 6px 10px; background: #e5e5ea; border-radius: 8px; }}
  .deck-title {{ font-size: 15px; font-weight: 600; color: #3a3a3c; }}
  .btn-reset {{ padding: 6px 12px; font-size: 13px; background: #e5e5ea; border: none; border-radius: 8px; cursor: pointer; }}
  .card-box {{ width: 100%; max-width: 680px; min-height: 380px; height: 52vh; perspective: 1200px; cursor: pointer; }}
  .card-inner {{ width: 100%; height: 100%; position: relative; transform-style: preserve-3d; transition: transform 0.35s; border-radius: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.07); }}
  .card-inner.flipped {{ transform: rotateY(180deg); }}
  .card-face {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; background: var(--card-bg); border-radius: 18px; display: flex; justify-content: center; align-items: center; padding: 14px; box-sizing: border-box; }}
  .card-back {{ transform: rotateY(180deg); background: #fafbfc; }}
  .card-face img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
  .badge {{ position: absolute; top: 12px; left: 16px; font-size: 11px; font-weight: 700; color: #aeaeb2; }}
  .prog-tag {{ position: absolute; top: 12px; right: 16px; font-size: 12px; color: #8e8e93; font-weight: 600; }}
  .controls {{ display: flex; gap: 12px; width: 100%; max-width: 680px; margin-top: 18px; }}
  button.action-btn {{ flex: 1; padding: 15px; border-radius: 12px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; }}
  .btn-flip {{ background: var(--primary); color: #fff; }}
  .btn-again {{ background: #ffebeb; color: var(--danger); }}
  .btn-pass {{ background: #e6f9ed; color: var(--success); }}
</style>
</head>
<body>
  <div class="header">
    <a href="indexcards.html" class="nav-back">‹ 目录</a>
    <div class="deck-title">9结构综合97</div>
    <button class="btn-reset" onclick="resetDeck()">重置本轮</button>
  </div>
  <div class="card-box" onclick="flipCard()">
    <div class="card-inner" id="cardInner">
      <div class="card-face card-front">
        <span class="badge">正面 / 题目</span>
        <span class="prog-tag" id="prog"></span>
        <img id="fImg" src="">
      </div>
      <div class="card-face card-back">
        <span class="badge">背面 / 答案</span>
        <img id="bImg" src="">
      </div>
    </div>
  </div>
  <div class="controls">
    <button class="action-btn btn-flip" onclick="flipCard()">翻转</button>
    <button class="action-btn btn-again" onclick="rate(false)">没记住 (重排)</button>
    <button class="action-btn btn-pass" onclick="rate(true)">记住了 (移出)</button>
  </div>
  <script>
    const deck = {cards_json};
    let queue = [...deck];
    let isFlipped = false;
    function update() {{
      isFlipped = false;
      document.getElementById('cardInner').classList.remove('flipped');
      if (queue.length === 0) {{
        document.getElementById('prog').innerText = '🎉 已背完！';
        document.getElementById('fImg').src = '';
        document.getElementById('bImg').src = '';
        return;
      }}
      document.getElementById('prog').innerText = '剩余 ' + queue.length + ' / ' + deck.length;
      document.getElementById('fImg').src = queue[0].front;
      document.getElementById('bImg').src = queue[0].back;
    }}
    function flipCard() {{
      if (queue.length === 0) return;
      isFlipped = !isFlipped;
      document.getElementById('cardInner').classList.toggle('flipped', isFlipped);
    }}
    function rate(pass) {{
      if (queue.length === 0) return;
      if (pass) {{ queue.shift(); }} else {{ queue.push(queue.shift()); }}
      update();
    }}
    function resetDeck() {{ queue = [...deck]; update(); }}
    update();
  </script>
</body>
</html>"""
            with open("9结构综合97.html", "w", encoding="utf-8") as f_out:
                f_out.write(chapter_html)
                
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"🎉 保存成功！已重新生成 9结构综合97.html，包含 {len(cards)} 题！直接推送到 GitHub 即可。".encode('utf-8'))
        else:
            super().do_GET()

print("\n🚀 整理器启动中...")
print("👉 请在浏览器打开地址： http://localhost:8899/sorter.html")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", 8899), Handler) as httpd:
    httpd.serve_forever()
