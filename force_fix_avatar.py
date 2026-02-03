import os

avatar_url = "https://images.unsplash.com/photo-1541364983171-a8ba01d95cfc?q=80&w=256&h=256&auto=format&fit=crop"
new_avatar_html = f'''                    <div class="relative">
                        <img src="{avatar_url}" class="w-10 h-10 rounded-full border-2 border-blue-500 shadow-lg object-cover">
                        <span class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-[#161a1e] rounded-full animate-pulse"></span>
                    </div>'''

files = ['index.html', 'battle-station.html', 'project-management.html', 'reports.html']

for filename in files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尋找頭像區塊並替換
    start_marker = '<div class="relative">'
    end_marker = '</div>'
    
    # 在側邊欄範圍內尋找
    sidebar_start = content.find('<!-- Sidebar -->')
    if sidebar_start != -1:
        target_start = content.find(start_marker, sidebar_start)
        target_end = content.find(end_marker, target_start) + len(end_marker)
        
        if target_start != -1:
            new_content = content[:target_start] + new_avatar_html + content[target_end:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed avatar in {filename}")

os.system("git add . && git commit -m 'FORCE FIX: Show Aliple Avatar on all pages' && git push origin main")
