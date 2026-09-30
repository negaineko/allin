import json, os, zipfile, shutil, hashlib

with open("order_rules.json", "r", encoding="utf-8") as f:
    order_rules = json.load(f)

key = next((k for k in order_rules.keys() if "结构综合" in k), None)
if not key:
    print("❌ 未找到【结构综合】规则")
    exit(1)

seq = order_rules[key]

# 查找 9结构综合97.goodnotes 文件
gn_files = [f for f in os.listdir('.') if f.endswith('.goodnotes')]
jg_gn = next((f for f in gn_files if "结构综合" in f), None)
if not jg_gn:
    for p in ["..", os.path.expanduser("~/Desktop/cards"), os.path.expanduser("~/Desktop/allin")]:
        cand = os.path.join(p, "9结构综合97.goodnotes")
        if os.path.exists(cand):
            jg_gn = cand
            break

if not jg_gn:
    print("❌ 未找到 9结构综合97.goodnotes")
    exit(1)

# 计算每个附件的 MD5，精准找出完全相同的两张图
hashes = {}
duplicate_attachment = None

with zipfile.ZipFile(jg_gn, 'r') as z:
    # 只需要比对前 40 张图片（第 8 题一般在前 20-30 项内）
    for src in seq[:40]:
        try:
            data = z.read(src)
            h = hashlib.md5(data).hexdigest()
            if h in hashes:
                duplicate_attachment = src
                print(f"🎯 找到完全重复的图片素材: {src} (MD5: {h})")
                break
            hashes[h] = src
        except Exception:
            continue

# 如果附件本身引用了相同文件名，或者两处引用了同一个文件
if not duplicate_attachment:
    # 检查 seq 列表中是否有完全同名的项
    seen = set()
    for s in seq:
        if s in seen:
            duplicate_attachment = s
            print(f"🎯 在序列中找到重复引用的文件名: {s}")
            break
        seen.add(s)

# 找出该图片出现的所有下标位置
occurrences = []
with zipfile.ZipFile(jg_gn, 'r') as z:
    target_hash = None
    if duplicate_attachment:
        target_hash = hashlib.md5(z.read(duplicate_attachment)).hexdigest()
        for idx, src in enumerate(seq):
            try:
                if hashlib.md5(z.read(src)).hexdigest() == target_hash:
                    occurrences.append(idx)
            except Exception:
                pass

print(f"该图片在序列中出现的位置下标: {occurrences}")

if len(occurrences) >= 2:
    del_idx = occurrences[1] # 严格删除第 2 次出现的
    removed_item = seq.pop(del_idx)
    print(f"🗑️ 成功剔除第 2 次出现的图片（索引 #{del_idx}）: {removed_item}")
    
    with open("order_rules.json", "w", encoding="utf-8") as f_w:
        json.dump(order_rules, f_w, ensure_ascii=False, indent=2)
else:
    print("⚠️ 未自动检测到完全相同的 MD5，按位置兜底检查（第 8 题附近）")
    # 如果两张图不是二进制完全一样（如略微缩放），可直接指定第 8 题答案的第 2 次下标
    # 若需手动指定，可在确认下标后执行

# 重新生成 HTML 与图片
out_images_dir = "images"
safe_prefix = "9结构综合97"
final_img_paths = []

with zipfile.ZipFile(jg_gn, 'r') as z:
    for idx, src in enumerate(seq):
        out_name = f"{safe_prefix}_{len(final_img_paths):03d}.jpg"
        out_file = os.path.join(out_images_dir, out_name)
        try:
            with open(out_file, "wb") as f_img:
                f_img.write(z.read(src))
            final_img_paths.append(f"images/{out_name}")
        except Exception:
            continue

        if idx == 146:
            ans_pic = next((f for f in ["6_32_ans.jpg", "6_32_ans.png"] if os.path.exists(f)), None)
            if ans_pic:
                ext = os.path.splitext(ans_pic)[1]
                ans_name = f"{safe_prefix}_{len(final_img_paths):03d}{ext}"
                shutil.copy(ans_pic, os.path.join(out_images_dir, ans_name))
                final_img_paths.append(f"images/{ans_name}")

cards = []
for i in range(0, len(final_img_paths) - 1, 2):
    cards.append({
        "id": i // 2 + 1,
        "front": final_img_paths[i],
        "back": final_img_paths[i + 1]
    })

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
  .deck-title {{ font-size: 15px; font-weight: 600; color: #3a3a3c; max-width: 45%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .btn-reset {{ padding: 6px 12px; font-size: 13px; background: #e5e5ea; border: none; border-radius: 8px; cursor: pointer; color: #1c1c1e; font-weight: 500; }}
  .card-box {{ width: 100%; max-width: 680px; min-height: 380px; max-height: 62vh; height: 52vh; perspective: 1200px; cursor: pointer; }}
  .card-inner {{ width: 100%; height: 100%; position: relative; transform-style: preserve-3d; transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1); border-radius: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.07); }}
  .card-inner.flipped {{ transform: rotateY(180deg); }}
  .card-face {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; background: var(--card-bg); border-radius: 18px; display: flex; justify-content: center; align-items: center; padding: 14px; box-sizing: border-box; overflow: hidden; }}
  .card-back {{ transform: rotateY(180deg); background: #fafbfc; }}
  .card-face img {{ max-width: 100%; max-height: 100%; object-fit: contain; pointer-events: none; }}
  .badge {{ position: absolute; top: 12px; left: 16px; font-size: 11px; font-weight: 700; color: #aeaeb2; letter-spacing: 0.5px; }}
  .prog-tag {{ position: absolute; top: 12px; right: 16px; font-size: 12px; color: #8e8e93; font-weight: 600; }}
  .controls {{ display: flex; gap: 12px; width: 100%; max-width: 680px; margin-top: 18px; }}
  button.action-btn {{ flex: 1; padding: 15px; border-radius: 12px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.1s; }}
  button.action-btn:active {{ transform: scale(0.97); }}
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
        <img id="fImg" src="" alt="题目">
      </div>
      <div class="card-face card-back">
        <span class="badge">背面 / 答案</span>
        <img id="bImg" src="" alt="答案">
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

print(f"\n🎉 重新构建完毕！当前总题数为 {len(cards)} 题。")
