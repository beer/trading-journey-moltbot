import urllib.request
import json
import time

def test_api():
    base_url = "http://127.0.0.1/api/tasks"
    print("🚀 Starting API Integration Test...")
    
    # 1. Test GET
    try:
        res = urllib.request.urlopen(base_url)
        tasks = json.loads(res.read())
        print(f"✅ GET Success: Found {len(tasks)} tasks")
    except Exception as e:
        print(f"❌ GET Failed: {e}")
        return

    # 2. Test POST (Add)
    try:
        data = json.dumps({"title": "Test Task", "description": "Automated Test"}).encode()
        req = urllib.request.Request(base_url, data=data, method='POST')
        res = urllib.request.urlopen(req)
        new_task = json.loads(res.read())
        task_id = new_task['id']
        print(f"✅ POST Success: Created task ID {task_id}")
    except Exception as e:
        print(f"❌ POST Failed: {e}")
        return

    # 3. Test PUT (Update)
    try:
        update_url = f"{base_url}/{task_id}"
        data = json.dumps({"status": "done"}).encode()
        req = urllib.request.Request(update_url, data=data, method='PUT')
        urllib.request.urlopen(req)
        print(f"✅ PUT Success: Updated task {task_id}")
    except Exception as e:
        print(f"❌ PUT Failed: {e}")
        return

    # 4. Test DELETE
    try:
        delete_url = f"{base_url}/{task_id}"
        req = urllib.request.Request(delete_url, method='DELETE')
        urllib.request.urlopen(req)
        print(f"✅ DELETE Success: Cleaned up test task")
    except Exception as e:
        print(f"❌ DELETE Failed: {e}")
        return

    print("🎉 ALL TESTS PASSED! API is ready.")

if __name__ == "__main__":
    test_api()
