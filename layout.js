async function loadSidebar() {
    try {
        const response = await fetch('sidebar.html');
        const html = await response.text();
        document.getElementById('sidebar-container').innerHTML = html;
        
        // 根據當前頁面高亮對應標籤
        const currentPage = window.location.pathname.split("/").pop() || "index.html";
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            if (item.getAttribute('href') === currentPage) {
                item.classList.add('bg-blue-600/10', 'border-l-4', 'border-blue-500', 'text-blue-400');
                item.classList.remove('text-gray-400');
            }
        });
    } catch (err) {
        console.error('Failed to load sidebar:', err);
    }
}
loadSidebar();

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('active');
}
