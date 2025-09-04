document.getElementById('theme-toggle').addEventListener('click', () => {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
});

document.getElementById('check-update').addEventListener('click', () => {
    alert('这里可以调用 Tauri 后端检查更新逻辑');
});
