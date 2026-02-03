import os

def run_test():
    pages = ['index.html', 'battle-station.html', 'project-management.html', 'reports.html']
    required_links = ['index.html', 'battle-station.html', 'project-management.html', 'reports.html']
    
    print("🚀 Running UI Automation Test...")
    all_pass = True
    
    for page in pages:
        if not os.path.exists(page):
            print(f"❌ Error: {page} is missing!")
            all_pass = False
            continue
            
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. 檢查 Sidepanel
        if 'id="sidebar"' not in content and '<!-- Sidebar -->' not in content:
            print(f"❌ Error: {page} is missing sidepanel container!")
            all_pass = False
            
        # 2. 檢查導覽連結
        for link in required_links:
            if f'href="{link}"' not in content:
                print(f"❌ Error: {page} is missing link to {link}!")
                all_pass = False
                
        # 3. 檢查頭像
        if 'aliple.jpg' not in content:
            print(f"❌ Error: {page} is missing Aliple's avatar!")
            all_pass = False

    if all_pass:
        print("✅ ALL UI TESTS PASSED! Ready to deploy.")
    return all_pass

if __name__ == "__main__":
    run_test()
