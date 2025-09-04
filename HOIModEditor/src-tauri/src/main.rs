#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::Manager;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("你好, {}! 来自 Rust 核心的问候~", name)
}

#[cfg(target_os = "windows")]
fn enable_mica_alt(window: &tauri::WebviewWindow) {
    use std::ffi::c_void;
    use windows::Win32::Graphics::Dwm::{
        DwmSetWindowAttribute, DWMWINDOWATTRIBUTE, DWMWA_SYSTEMBACKDROP_TYPE,
    };
    use windows::Win32::Foundation::HWND;

    unsafe {
        let hwnd: HWND = window.hwnd().unwrap();
        let backdrop_type: i32 = 2; // 2 = Mica Alt
        let _ = DwmSetWindowAttribute(
            hwnd,
            DWMWINDOWATTRIBUTE(DWMWA_SYSTEMBACKDROP_TYPE.0),
            &backdrop_type as *const _ as *const c_void,
            std::mem::size_of_val(&backdrop_type) as u32,
        );
    }
}

#[cfg(target_os = "windows")]
fn set_immersive_dark_mode(window: &tauri::WebviewWindow, dark: bool) {
    use std::ffi::c_void;
    use windows::Win32::Foundation::HWND;
    use windows::Win32::Graphics::Dwm::{
        DwmSetWindowAttribute, DWMWINDOWATTRIBUTE, DWMWA_USE_IMMERSIVE_DARK_MODE,
    };

    unsafe {
        let hwnd: HWND = window.hwnd().unwrap();
        // 直接用 i32 代替 BOOL
        let dark_mode: i32 = if dark { 1 } else { 0 };
        let _ = DwmSetWindowAttribute(
            hwnd,
            DWMWINDOWATTRIBUTE(DWMWA_USE_IMMERSIVE_DARK_MODE.0),
            &dark_mode as *const _ as *const c_void,
            std::mem::size_of_val(&dark_mode) as u32,
        );
    }
}

#[cfg(target_os = "windows")]
#[tauri::command]
fn set_theme(dark: bool, app: tauri::AppHandle) -> Result<(), String> {
    if let Some(w) = app.get_webview_window("main") {
        set_immersive_dark_mode(&w, dark);
        enable_mica_alt(&w); // 切换主题时重新应用 Mica Alt
        Ok(())
    } else {
        Err("未找到窗口 main".into())
    }
}

#[cfg(not(target_os = "windows"))]
#[tauri::command]
fn set_theme(_dark: bool, _app: tauri::AppHandle) -> Result<(), String> {
    Ok(())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, set_theme])
        .setup(|app| {
            #[cfg(target_os = "windows")]
            {
                if let Some(window) = app.get_webview_window("main") {
                    enable_mica_alt(&window);
                    // 可选：启动时根据系统主题初始化
                    // set_immersive_dark_mode(&window, false);
                }
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("运行 Tauri 失败");
}
