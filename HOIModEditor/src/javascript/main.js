const mainContent = document.getElementById('main-content');
const settingsBtn = document.getElementById('settings-btn');

settingsBtn.addEventListener('click', e => {
    e.preventDefault();
    loadSettingsPage();
});

function loadSettingsPage() {
    mainContent.innerHTML = `
        <div class="settings-page">
            <h1>设置</h1>

            <div class="settings-section">
                <h2>主题</h2>
                <div class="settings-option">
                    <span>浅色 / 深色模式</span>
                    <button id="theme-toggle">切换</button>
                </div>
            </div>

            <div class="settings-section">
                <h2>应用</h2>
                <div class="settings-option">
                    <span>检查更新</span>
                    <button id="check-update">检查</button>
                </div>
            </div>
        </div>
    `;

    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    document.getElementById('check-update').addEventListener('click', () => {
        alert('这里可以调用 Tauri 后端检查更新逻辑');
    });
}

function toggleTheme() {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
}
