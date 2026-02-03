import os

def sync():
    # 讀取 index.html 作為側邊欄模板
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 <aside> 區塊
    start_tag = '<!-- Sidebar -->'
    end_tag = '</aside>'
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag) + len(end_tag)
    
    if start_idx == -1:
        print("Error: Could not find Sidebar tag in index.html")
        return
        
    sidebar_html = content[start_idx:end_idx]
    
    # 需要同步的檔案清單
    target_files = ['battle-station.html', 'project-management.html', 'reports.html']
    
    for filename in target_files:
        if not os.path.exists(filename): continue
        
        with open(filename, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        t_start = target_content.find(start_tag)
        t_end = target_content.find(end_tag) + len(end_tag)
        
        if t_start != -1:
            new_content = target_content[:t_start] + sidebar_html + target_content[t_end:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Successfully synced UI to {filename}")

if __name__ == "__main__":
    sync()
