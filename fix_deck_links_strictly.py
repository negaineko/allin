import os, re

# 排除目录主页自身与临时工具
EXCLUDE = {"index.html", "indexcards.html", "sorter.html", "drag_sorter.html"}
all_html = [f for f in os.listdir('.') if f.endswith('.html') and f not in EXCLUDE]

modified_decks = []
skipped_files = []

for fname in all_html:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # 严格判断特征：只要包含 cardInner 或 deck-title，才判定为刷题卡
    is_flashcard = ("cardInner" in content) or ("deck-title" in content)

    if is_flashcard:
        # 仅对刷题卡页面将指向 index.html 的返回链接改为 indexcards.html
        new_content = re.sub(r'href=["\'](index|\./index)\.html["\']', 'href="indexcards.html"', content)
        if new_content != content:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_decks.append(fname)
            print(f"🃏 刷题卡返回链接已修正 -> indexcards.html: {fname}")
        else:
            print(f"✅ 刷题卡链接已经是 indexcards.html: {fname}")
    else:
        # 非简答题页面：完全不作任何修改与触碰
        skipped_files.append(fname)

print(f"\n🎉 运行完成！")
print(f"• 仅修改了 {len(modified_decks)} 个简答题刷题卡文件。")
print(f"• 严格跳过了 {len(skipped_files)} 个非简答题页面（填空、选择题等原封不动，未做任何触碰）。")
