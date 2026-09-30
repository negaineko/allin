import json, os, shutil

# 1. 194张卡片的完整正确列表
items = [{"src":"images/jiegou_raw_000.jpg","type":"gn"},{"src":"images/jiegou_raw_001.jpg","type":"gn"},{"src":"images/jiegou_raw_002.jpg","type":"gn"},{"src":"images/jiegou_raw_003.jpg","type":"gn"},{"src":"images/jiegou_raw_004.jpg","type":"gn"},{"src":"images/jiegou_raw_005.jpg","type":"gn"},{"src":"images/jiegou_raw_006.jpg","type":"gn"},{"src":"images/jiegou_raw_007.jpg","type":"gn"},{"src":"images/jiegou_raw_008.jpg","type":"gn"},{"src":"images/jiegou_raw_009.jpg","type":"gn"},{"src":"images/jiegou_raw_010.jpg","type":"gn"},{"src":"images/jiegou_raw_011.jpg","type":"gn"},{"src":"images/jiegou_raw_013.jpg","type":"gn"},{"src":"images/jiegou_raw_014.jpg","type":"gn"},{"src":"images/jiegou_raw_015.jpg","type":"gn"},{"src":"images/jiegou_raw_016.jpg","type":"gn"},{"src":"images/jiegou_raw_017.jpg","type":"gn"},{"src":"images/jiegou_raw_018.jpg","type":"gn"},{"src":"images/jiegou_raw_019.jpg","type":"gn"},{"src":"images/jiegou_raw_021.jpg","type":"gn"},{"src":"images/jiegou_raw_022.jpg","type":"gn"},{"src":"images/jiegou_raw_023.jpg","type":"gn"},{"src":"images/jiegou_raw_024.jpg","type":"gn"},{"src":"images/jiegou_raw_025.jpg","type":"gn"},{"src":"images/jiegou_raw_027.jpg","type":"gn"},{"src":"images/jiegou_raw_028.jpg","type":"gn"},{"src":"images/jiegou_raw_029.jpg","type":"gn"},{"src":"images/jiegou_raw_030.jpg","type":"gn"},{"src":"images/jiegou_raw_031.jpg","type":"gn"},{"src":"images/jiegou_raw_032.jpg","type":"gn"},{"src":"images/jiegou_raw_033.jpg","type":"gn"},{"src":"images/jiegou_raw_034.jpg","type":"gn"},{"src":"images/jiegou_raw_035.jpg","type":"gn"},{"src":"images/jiegou_raw_036.jpg","type":"gn"},{"src":"images/jiegou_raw_037.jpg","type":"gn"},{"src":"images/jiegou_raw_038.jpg","type":"gn"},{"src":"images/jiegou_raw_039.jpg","type":"gn"},{"src":"images/jiegou_raw_040.jpg","type":"gn"},{"src":"images/jiegou_raw_041.jpg","type":"gn"},{"src":"images/jiegou_raw_042.jpg","type":"gn"},{"src":"images/jiegou_raw_043.jpg","type":"gn"},{"src":"images/jiegou_raw_044.jpg","type":"gn"},{"src":"images/jiegou_raw_045.jpg","type":"gn"},{"src":"images/jiegou_raw_046.jpg","type":"gn"},{"src":"images/jiegou_raw_047.jpg","type":"gn"},{"src":"images/jiegou_raw_048.jpg","type":"gn"},{"src":"images/jiegou_raw_049.jpg","type":"gn"},{"src":"images/jiegou_raw_050.jpg","type":"gn"},{"src":"images/jiegou_raw_051.jpg","type":"gn"},{"src":"images/jiegou_raw_052.jpg","type":"gn"},{"src":"images/jiegou_raw_053.jpg","type":"gn"},{"src":"images/jiegou_raw_054.jpg","type":"gn"},{"src":"images/jiegou_raw_055.jpg","type":"gn"},{"src":"images/jiegou_raw_056.jpg","type":"gn"},{"src":"images/jiegou_raw_057.jpg","type":"gn"},{"src":"images/jiegou_raw_059.jpg","type":"gn"},{"src":"images/jiegou_raw_058.jpg","type":"gn"},{"src":"images/jiegou_raw_060.jpg","type":"gn"},{"src":"images/jiegou_raw_061.jpg","type":"gn"},{"src":"images/drag_custom_1790731841760.png","type":"custom"},{"src":"images/jiegou_raw_062.jpg","type":"gn"},{"src":"images/jiegou_raw_063.jpg","type":"gn"},{"src":"images/jiegou_raw_064.jpg","type":"gn"},{"src":"images/drag_custom_1790731974648.png","type":"custom"},{"src":"images/jiegou_raw_065.jpg","type":"gn"},{"src":"images/drag_custom_1790732141294.png","type":"custom"},{"src":"images/jiegou_raw_066.jpg","type":"gn"},{"src":"images/jiegou_raw_067.jpg","type":"gn"},{"src":"images/jiegou_raw_068.jpg","type":"gn"},{"src":"images/drag_custom_1790732277268.png","type":"custom"},{"src":"images/jiegou_raw_069.jpg","type":"gn"},{"src":"images/jiegou_raw_070.jpg","type":"gn"},{"src":"images/jiegou_raw_071.jpg","type":"gn"},{"src":"images/jiegou_raw_072.jpg","type":"gn"},{"src":"images/jiegou_raw_074.jpg","type":"gn"},{"src":"images/jiegou_raw_073.jpg","type":"gn"},{"src":"images/jiegou_raw_075.jpg","type":"gn"},{"src":"images/jiegou_raw_076.jpg","type":"gn"},{"src":"images/jiegou_raw_078.jpg","type":"gn"},{"src":"images/jiegou_raw_077.jpg","type":"gn"},{"src":"images/jiegou_raw_080.jpg","type":"gn"},{"src":"images/jiegou_raw_081.jpg","type":"gn"},{"src":"images/jiegou_raw_083.jpg","type":"gn"},{"src":"images/jiegou_raw_084.jpg","type":"gn"},{"src":"images/jiegou_raw_082.jpg","type":"gn"},{"src":"images/jiegou_raw_085.jpg","type":"gn"},{"src":"images/jiegou_raw_086.jpg","type":"gn"},{"src":"images/jiegou_raw_087.jpg","type":"gn"},{"src":"images/jiegou_raw_088.jpg","type":"gn"},{"src":"images/jiegou_raw_089.jpg","type":"gn"},{"src":"images/jiegou_raw_090.jpg","type":"gn"},{"src":"images/jiegou_raw_091.jpg","type":"gn"},{"src":"images/jiegou_raw_092.jpg","type":"gn"},{"src":"images/jiegou_raw_093.jpg","type":"gn"},{"src":"images/jiegou_raw_094.jpg","type":"gn"},{"src":"images/jiegou_raw_095.jpg","type":"gn"},{"src":"images/jiegou_raw_096.jpg","type":"gn"},{"src":"images/jiegou_raw_097.jpg","type":"gn"},{"src":"images/jiegou_raw_098.jpg","type":"gn"},{"src":"images/jiegou_raw_099.jpg","type":"gn"},{"src":"images/jiegou_raw_100.jpg","type":"gn"},{"src":"images/jiegou_raw_101.jpg","type":"gn"},{"src":"images/jiegou_raw_102.jpg","type":"gn"},{"src":"images/jiegou_raw_103.jpg","type":"gn"},{"src":"images/jiegou_raw_104.jpg","type":"gn"},{"src":"images/jiegou_raw_105.jpg","type":"gn"},{"src":"images/jiegou_raw_106.jpg","type":"gn"},{"src":"images/jiegou_raw_107.jpg","type":"gn"},{"src":"images/jiegou_raw_109.jpg","type":"gn"},{"src":"images/jiegou_raw_108.jpg","type":"gn"},{"src":"images/jiegou_raw_110.jpg","type":"gn"},{"src":"images/jiegou_raw_111.jpg","type":"gn"},{"src":"images/jiegou_raw_112.jpg","type":"gn"},{"src":"images/jiegou_raw_113.jpg","type":"gn"},{"src":"images/jiegou_raw_114.jpg","type":"gn"},{"src":"images/drag_custom_1790732487090.png","type":"custom"},{"src":"images/jiegou_raw_115.jpg","type":"gn"},{"src":"images/jiegou_raw_116.jpg","type":"gn"},{"src":"images/jiegou_raw_117.jpg","type":"gn"},{"src":"images/jiegou_raw_118.jpg","type":"gn"},{"src":"images/jiegou_raw_119.jpg","type":"gn"},{"src":"images/jiegou_raw_120.jpg","type":"gn"},{"src":"images/jiegou_raw_121.jpg","type":"gn"},{"src":"images/jiegou_raw_122.jpg","type":"gn"},{"src":"images/jiegou_raw_123.jpg","type":"gn"},{"src":"images/jiegou_raw_124.jpg","type":"gn"},{"src":"images/jiegou_raw_125.jpg","type":"gn"},{"src":"images/jiegou_raw_126.jpg","type":"gn"},{"src":"images/jiegou_raw_129.jpg","type":"gn"},{"src":"images/jiegou_raw_127.jpg","type":"gn"},{"src":"images/jiegou_raw_130.jpg","type":"gn"},{"src":"images/jiegou_raw_128.jpg","type":"gn"},{"src":"images/jiegou_raw_131.jpg","type":"gn"},{"src":"images/jiegou_raw_132.jpg","type":"gn"},{"src":"images/jiegou_raw_133.jpg","type":"gn"},{"src":"images/jiegou_raw_136.jpg","type":"gn"},{"src":"images/jiegou_raw_134.jpg","type":"gn"},{"src":"images/jiegou_raw_137.jpg","type":"gn"},{"src":"images/jiegou_raw_135.jpg","type":"gn"},{"src":"images/jiegou_raw_139.jpg","type":"gn"},{"src":"images/jiegou_raw_141.jpg","type":"gn"},{"src":"images/jiegou_raw_140.jpg","type":"gn"},{"src":"images/jiegou_raw_142.jpg","type":"gn"},{"src":"images/jiegou_raw_143.jpg","type":"gn"},{"src":"images/jiegou_raw_144.jpg","type":"gn"},{"src":"images/jiegou_raw_145.jpg","type":"gn"},{"src":"images/jiegou_raw_146.jpg","type":"gn"},{"src":"images/drag_custom_1790732785320.png","type":"custom"},{"src":"images/jiegou_raw_147.jpg","type":"gn"},{"src":"images/jiegou_raw_149.jpg","type":"gn"},{"src":"images/jiegou_raw_148.jpg","type":"gn"},{"src":"images/jiegou_raw_150.jpg","type":"gn"},{"src":"images/jiegou_raw_151.jpg","type":"gn"},{"src":"images/jiegou_raw_152.jpg","type":"gn"},{"src":"images/jiegou_raw_153.jpg","type":"gn"},{"src":"images/jiegou_raw_154.jpg","type":"gn"},{"src":"images/jiegou_raw_155.jpg","type":"gn"},{"src":"images/jiegou_raw_156.jpg","type":"gn"},{"src":"images/jiegou_raw_157.jpg","type":"gn"},{"src":"images/jiegou_raw_158.jpg","type":"gn"},{"src":"images/jiegou_raw_159.jpg","type":"gn"},{"src":"images/jiegou_raw_160.jpg","type":"gn"},{"src":"images/jiegou_raw_161.jpg","type":"gn"},{"src":"images/jiegou_raw_162.jpg","type":"gn"},{"src":"images/jiegou_raw_163.jpg","type":"gn"},{"src":"images/jiegou_raw_164.jpg","type":"gn"},{"src":"images/jiegou_raw_165.jpg","type":"gn"},{"src":"images/jiegou_raw_166.jpg","type":"gn"},{"src":"images/jiegou_raw_168.jpg","type":"gn"},{"src":"images/jiegou_raw_167.jpg","type":"gn"},{"src":"images/jiegou_raw_169.jpg","type":"gn"},{"src":"images/jiegou_raw_170.jpg","type":"gn"},{"src":"images/jiegou_raw_171.jpg","type":"gn"},{"src":"images/jiegou_raw_173.jpg","type":"gn"},{"src":"images/jiegou_raw_172.jpg","type":"gn"},{"src":"images/jiegou_raw_174.jpg","type":"gn"},{"src":"images/jiegou_raw_175.jpg","type":"gn"},{"src":"images/jiegou_raw_176.jpg","type":"gn"},{"src":"images/jiegou_raw_177.jpg","type":"gn"},{"src":"images/jiegou_raw_178.jpg","type":"gn"},{"src":"images/jiegou_raw_179.jpg","type":"gn"},{"src":"images/jiegou_raw_180.jpg","type":"gn"},{"src":"images/jiegou_raw_181.jpg","type":"gn"},{"src":"images/jiegou_raw_182.jpg","type":"gn"},{"src":"images/jiegou_raw_183.jpg","type":"gn"},{"src":"images/jiegou_raw_185.jpg","type":"gn"},{"src":"images/jiegou_raw_184.jpg","type":"gn"},{"src":"images/jiegou_raw_186.jpg","type":"gn"},{"src":"images/jiegou_raw_188.jpg","type":"gn"},{"src":"images/jiegou_raw_187.jpg","type":"gn"},{"src":"images/jiegou_raw_190.jpg","type":"gn"},{"src":"images/jiegou_raw_189.jpg","type":"gn"},{"src":"images/jiegou_raw_191.jpg","type":"gn"},{"src":"images/jiegou_raw_192.jpg","type":"gn"}]

os.makedirs("images", exist_ok=True)
safe_prefix = "9结构综合97"
final_img_paths = []

for idx, it in enumerate(items):
    ext = os.path.splitext(it["src"])[1] or ".jpg"
    target_name = f"{safe_prefix}_{idx:03d}{ext}"
    target_path = os.path.join("images", target_name)
    
    src_path = it["src"]
    if os.path.exists(src_path):
        if os.path.abspath(src_path) != os.path.abspath(target_path):
            shutil.copy(src_path, target_path)
    
    # 加上时间戳版本号强制更新缓存
    mtime = int(os.path.getmtime(target_path)) if os.path.exists(target_path) else idx
    final_img_paths.append(f"images/{target_name}?v={mtime}")

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

print(f"\n🎉 完美构建成功！共打包成对卡片: {len(cards)} 题（共 194 张图）！")
