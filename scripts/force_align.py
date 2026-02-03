import os

# 這是我們完美的側邊欄母本
sidebar_template = '''
    <!-- Sidebar -->
    <aside id="sidebar" class="sidebar w-64 bg-[#161a1e] border-r border-gray-800 flex flex-col fixed inset-y-0 left-0 md:relative md:translate-x-0">
        <div class="p-6 border-b border-gray-800 hidden md:block">
            <h1 class="text-xl font-bold text-blue-400 flex items-center"><span class="bg-blue-500 text-white p-1 rounded mr-2 text-xs">CM</span> Crazy Money</h1>
        </div>
        <nav class="flex-1 mt-4">
            <a href="index.html" class="flex items-center px-6 py-3 text-gray-400 hover:bg-gray-800 transition"><i class="fas fa-th-large mr-3"></i> Dashboard</a>
            <a href="battle-station.html" class="flex items-center px-6 py-3 text-gray-400 hover:bg-gray-800 transition"><i class="fas fa-bolt mr-3"></i> Battle Station</a>
            <a href="project-management.html" class="flex items-center px-6 py-3 text-gray-400 hover:bg-gray-800 transition"><i class="fas fa-tasks mr-3"></i> Project Kanban</a>
            <a href="reports.html" class="flex items-center px-6 py-3 text-gray-400 hover:bg-gray-800 transition"><i class="fas fa-file-alt mr-3"></i> AI Reports</a>
        </nav>
        <div class="p-6 border-t border-gray-800">
            <div class="flex items-center space-x-3">
                <img src="aliple.jpg" class="w-10 h-10 rounded-full border-2 border-blue-500 object-cover shadow-lg shadow-blue-500/20">
                <div class="text-[10px]"><p class="text-gray-500 font-bold uppercase">Aliple</p><p class="text-blue-400">正在守護您的交易...</p></div>
            </div>
        </div>
    </aside>
'''

pages = ['index.html', 'battle-station.html', 'project-management.html', 'reports.html']

for page in pages:
    if not os.path.exists(page): continue
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 尋找舊的 sidebar 或 aside 標籤並進行暴力替換
    start_tag = '<aside'
    end_tag = '</aside>'
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag) + len(end_tag)
    
    if start_idx != -1:
        new_content = content[:start_idx] + sidebar_template + content[end_idx:]
        with open(page, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Force-aligned Sidebar in {page}")

os.system("git add . && git commit -m 'ULTIMATE SIDEBAR ALIGNMENT: 4 tabs restored' && git push origin main")
