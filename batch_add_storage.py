import os, re, hashlib

# 排除不需要处理的文件
EXCLUDE_FILES = {"16.html", "1212.html", "indexcards.html", "sorter.html", "drag_sorter.html"}

# 遍历当前目录所有的 html 文件
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in EXCLUDE_FILES]

def generate_script(deck_json, storage_key):
    return f"""<script>
    const STORAGE_KEY = '{storage_key}';
    const deck = {deck_json};
    
    // 读取本地保存的剩余队列，若没有则从全量题库开始
    function loadSavedQueue() {{
      try {{
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {{
          const parsed = JSON.parse(saved);
          if (Array.isArray(parsed) && parsed.length > 0) {{
            return parsed;
          }}
        }}
      }} catch (e) {{
        console.warn('读取本地进度失败，使用默认全量', e);
      }}
      return [...deck];
    }}

    let queue = loadSavedQueue();
    let isFlipped = false;

    function saveQueue() {{
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(queue));
      }} catch (e) {{
        console.warn('保存进度失败', e);
      }}
    }}

    function update() {{
      isFlipped = false;
      const inner = document.getElementById('cardInner');
      if (inner) inner.classList.remove('flipped');
      if (queue.length === 0) {{
        const p = document.getElementById('prog');
        if (p) p.innerText = '🎉 已背完！';
        const fi = document.getElementById('fImg');
        const bi = document.getElementById('bImg');
        if (fi) fi.src = '';
        if (bi) bi.src = '';
        saveQueue();
        return;
      }}
      const p = document.getElementById('prog');
      if (p) p.innerText = '剩余 ' + queue.length + ' / ' + deck.length;
      const fi = document.getElementById('fImg');
      const bi = document.getElementById('bImg');
      if (fi) fi.src = queue[0].front;
      if (bi) bi.src = queue[0].back;
      saveQueue();
    }}

    function flipCard() {{
      if (queue.length === 0) return;
      isFlipped = !isFlipped;
      const inner = document.getElementById('cardInner');
      if (inner) inner.classList.toggle('flipped', isFlipped);
    }}

    function rate(pass) {{
      if (queue.length === 0) return;
      if (pass) {{
        queue.shift();
      }} else {{
        queue.push(queue.shift());
      }}
      update();
    }}

    function resetDeck() {{
      if (confirm('确定要重置当前进度、重新背这一章吗？')) {{
        localStorage.removeItem(STORAGE_KEY);
        queue = [...deck];
        update();
      }}
    }}

    update();
  </script>"""

count = 0
for fname in html_files:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取题库的 deck 数组
    m = re.search(r"const deck = (\[.*?\]);", content, re.DOTALL)
    if not m:
        continue

    deck_json = m.group(1)
    
    # 用安全字符串作为 localStorage 的 Key
    clean_name = re.sub(r'[^\w\u4e00-\u9fa5]', '_', os.path.splitext(fname)[0])
    storage_key = f"flashcard_queue_{clean_name}"

    # 替换 <script> 逻辑
    old_script_pattern = re.compile(r"<script>.*?</script>", re.DOTALL)
    new_script_block = generate_script(deck_json, storage_key)
    
    new_content = old_script_pattern.sub(new_script_block, content)
    
    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ 已升级: {fname} -> 存储Key: {storage_key}")
    count += 1

print(f"\n🎉 全部处理完成！共为 {count} 个刷题卡页面增加了进度记忆功能。")
