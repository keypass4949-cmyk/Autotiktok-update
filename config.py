import copy
import json
import os
import sys
import threading

# --- XÁC ĐỊNH THƯ MỤC GỐC CHUẨN XÁC ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(current_dir) if os.path.basename(current_dir) in ['core', 'utils', 'ui'] else current_dir

CONFIG_DIR = os.path.join(BASE_DIR, "Config")
DATA_DIR = os.path.join(BASE_DIR, "Data")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
CONFIG_FILE = os.path.join(CONFIG_DIR, "script_config.json")
AI_KEYS_FILE = os.path.join(CONFIG_DIR, "ai_keys.txt")

APP_CHOICES = ["TIK STUDIO", "TIK THƯỜNG", "TIK WHEE"]
METHOD_CHOICES = ["USER|PASS", "HOTMAIL", "EFAKEMAIL", "MAILFORSPAM"]
MODE_CHOICES = [
    "CHỈ LOGIN", 
    "CHỈ CHANGE", 
    "REG ACC",
    "LOGIN ➔ ĐĂNG VIDEO",
    "LOGIN ➔ XEM VIDEO",
    "CHUYỂN ACC ➔ ĐĂNG VIDEO",
    "CHUYỂN ACC ➔ XEM VIDEO",
    "REG ACC ➔ ĐĂNG VIDEO"
]
# Mật khẩu TikTok cố định: chỉ dùng khi login mail bị bắt "Xác minh danh tính" bằng mật khẩu
TIKTOK_VERIFY_PASSWORD = "ert123123@"

DEFAULT_POST_DETAILS = {
    "video_count": "1",
    "video_max": "1",
    "delay_min": "5",
    "delay_max": "10",
    "folder_path": "",
    "use_video": 1,
    "video_folder": os.path.join(BASE_DIR, "Media", "Video"),
    "use_image": 0,
    "image_folder": "",
    "delete_after": 0,
    "use_caption": 1,
    "caption": "",
    "caption_option": "1_dong",
    "use_music": 0,
    "music_mode": "none",
    "music_list": "",
    "post_retries": "2",
}

DEFAULT_WATCH_DETAILS = {
    "vid_min": 1,
    "vid_max": 3,
    "delay_min": 3,
    "delay_max": 5,
    "watch_min": 5,
    "watch_max": 10,
    "reset_min": 15,
    "reset_max": 25,
    "link_list": "",
    "do_like": 0,
    "do_follow": 0,
    "do_cmt": 0,
    "cmt_list": "",
}


def music_mode_of(details):
    """
    Giữ hàm này để không làm lỗi logic cũ, nhưng hiện tại luôn trả về 'none'
    vì tính năng nhạc đã bị loại bỏ khỏi UI.
    """
    return "none"
    
DEFAULT_CONFIG = {
    "settings": {
        "general_app": "TIK STUDIO",
        "general_method": "USER|PASS",
        "general_mode": "CHỈ LOGIN",
        "device_start_delay": 10,
        "enable_login_tasks": False,
        "login_max": "8",
        "login_rest_seconds": 180,
        "login_rest_max": 180,
        "device_start_delay_max": 10,
        "run_limit_minutes": 0,
        "task_delay_minutes": 0,
        "repeat_rounds": 0,
        "repeat_enabled": False,  
        "reconnect_timeout_seconds": 0,     
        "max_recover_retries": 5,          
        "clean_ram_before_run": False,      
        "disable_tiktok_notifications": False,  
        "enable_change_tasks": False,
        "change_new_password": "",
        "change_current_password": "",
        "change_pass": False,
        "turn_on_2fa": False,
        "change_logout": False,
        "enable_script_tasks": False,
        "schedule_enabled": False,
        "schedule_mode": "CHỈ LOGIN",    # 🟢 Thêm giá trị mặc định cho chế độ hẹn giờ
        "schedule_start": "08:00",
        "schedule_end": "23:00",
        "schedule_days": [0, 1, 2, 3, 4, 5, 6],
        "schedule_auto_stop": True,
        
        # --- PROXY ---
        "proxy": {
            "type": "kiot",
            "location": "random",
            "raw_keys": [],
            "keys": {}
        },
        "kiot": {
            "current_api": "https://api.kiotproxy.com/api/v1/proxies/current?key={}",
            "new_api": "https://api.kiotproxy.com/api/v1/proxies/new?key={}&region={}"
        },
        "fproxy": {
            "current_api": "https://fproxy.me/api/getcurrent?api_key={}",
            "new_api": "https://fproxy.me/api/getnew?api_key={}&location={}"
        },
        
        "device_names": {},
        "device_notes": {},
        "auto_scan": False,
        "scan_interval": 5,
        "adb_group": "auto",
        "schedule_enabled": False,
        "schedule_start": "08:00",
        "schedule_end": "23:00",
        "schedule_days": [0, 1, 2, 3, 4, 5, 6],
        "schedule_auto_stop": False,
        "control_enabled": False,
        "control_port": 8765,
        "ui_theme": "dark",
        "account_source": "",
        "hidden_columns": [],
        "acc_columns_shown": [],   
        "verify_password": TIKTOK_VERIFY_PASSWORD,
        "last_apk_path": "",
        "last_wallpaper_path": "",
        "wifi_networks": [],
        "wifi_scope": "Máy đã chọn",
        "wifi_repeat": False,
        "proxy_list": [],
        "proxy_scope": "Máy đã chọn",
        "proxy_repeat": False,
        "proxy_enabled": False,
        "proxy_assigned": {},   
        "whee_name_file": "",   
        "whee_bio_file": "",   
        "whee_avatar_folder": "",
        "whee_phone_api_key": "",
        "whee_edit_name": False,
        "whee_edit_bio": False,
        "whee_edit_avatar": False,
        "whee_post_video": False,
        "ai_agents": [],        
        "ai_active": "",        
        "ai_fallback": "",        
        "ai_max_steps": 20,
        "ai_timeout": 300,
    },
    "script_list": [
        {"stt": "1", "name": "Đăng video", "details": DEFAULT_POST_DETAILS},
        {"stt": "2", "name": "Xem video", "details": DEFAULT_WATCH_DETAILS, "enabled": False},
    ],
    "actions": [],
    "campaigns": {}
}

_io_lock = threading.Lock()


def load_config():
    """Đọc cấu hình, trộn với mặc định (giữ cả các khóa lạ để không mất dữ liệu)."""
    cfg = copy.deepcopy(DEFAULT_CONFIG)
    if not os.path.exists(CONFIG_FILE):
        return cfg
    try:
        with _io_lock, open(CONFIG_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except Exception as e:
        print(f"Lỗi đọc file script_config.json: {e}")
        return cfg

    if isinstance(loaded, dict):
        if isinstance(loaded.get("settings"), dict):
            for key, value in loaded["settings"].items():
                cfg["settings"][key] = value
                
        if isinstance(loaded.get("script_list"), list) and loaded["script_list"]:
            cfg["script_list"] = loaded["script_list"]
        if isinstance(loaded.get("actions"), list):
            cfg["actions"] = loaded["actions"]
            
        if "campaigns" in loaded:
            cfg["campaigns"] = loaded.get("campaigns", {})

    names_present = {str(it.get("name", "")).strip().lower() for it in cfg["script_list"] if isinstance(it, dict)}
    for default_item in DEFAULT_CONFIG["script_list"]:
        if default_item["name"].strip().lower() not in names_present:
            cfg["script_list"].append(copy.deepcopy(default_item))
    return cfg


def get_verify_password():
    """Mật khẩu xác minh chung (Cài đặt chung); trống thì dùng mặc định."""
    return str(load_config()["settings"].get("verify_password") or "").strip() or TIKTOK_VERIFY_PASSWORD

def change_action(settings, **base):
    """Action CHANGE dựng từ settings — dùng chung cho pipeline và chạy riêng."""
    return {
        "task": "CHANGE",
        "change_new_password": settings.get("change_new_password", ""),
        "change_current_password": settings.get("change_current_password", ""),
        "details": {
            "change_pass": bool(settings.get("change_pass", False)),
            "turn_on_2fa": bool(settings.get("turn_on_2fa", False)),
            "remove_contact": bool(settings.get("change_remove_contact", False)),
            "replace_mail": bool(settings.get("change_replace_mail", False)),
            "logout_after": bool(settings.get("change_logout", True)),
        },
        **base,
    }

def get_post_details(cfg=None):
    cfg = cfg or load_config()
    for item in cfg.get("script_list", []):
        name = str(item.get("name", "")).lower()
        if "video" in name and "chỉ định" not in name and "xem video" not in name:
            raw = item.get("details", {}) or {}
            merged = dict(DEFAULT_POST_DETAILS)
            merged.update(raw)
            merged["music_mode"] = "none" # Đã vô hiệu hóa tính năng nhạc
            return merged
    return dict(DEFAULT_POST_DETAILS)
    
def _is_post_item(item):
    """Kiểm tra xem tác vụ có phải là Đăng video hay không."""
    name = str((item or {}).get("name", "")).strip().lower()
    return "video" in name and "chỉ định" not in name and "xem video" not in name


def is_watch_item(item):
    name = str((item or {}).get("name", "")).lower()
    return "chỉ định" in name or "xem video" in name


def get_watch_details(cfg=None):
    cfg = cfg or load_config()
    for item in cfg.get("script_list", []):
        if is_watch_item(item):
            raw = item.get("details", {}) or {}
            merged = dict(DEFAULT_WATCH_DETAILS)
            merged.update(raw)
            return merged
    return dict(DEFAULT_WATCH_DETAILS)


CHANGE_STEPS = ("change_pass", "turn_on_2fa")


def change_action(settings, **base):
    """Action CHANGE dựng từ settings — dùng chung cho pipeline và chạy riêng."""
    return {
        "task": "CHANGE",
        "change_new_password": settings.get("change_new_password", ""),
        "change_current_password": settings.get("change_current_password", ""),
        "details": {
            "change_pass": bool(settings.get("change_pass", False)),
            "turn_on_2fa": bool(settings.get("turn_on_2fa", False)),
            "logout_after": bool(settings.get("change_logout", False)),
        },
        **base,
    }


def change_steps_enabled(details):
    return any(details.get(k) for k in CHANGE_STEPS)


def compile_actions(settings, script_list):
    """Biên dịch danh sách tác vụ chạy CHÍNH XÁC theo 'CHẾ ĐỘ CHẠY' trên giao diện."""
    try:
        login_max_val = max(1, int(settings.get("login_max", 8)))
    except (TypeError, ValueError):
        login_max_val = 8

    gen_app = str(settings.get("general_app", "TIK STUDIO")).strip().upper()
    gen_method = settings.get("general_method", "USER|PASS")
    mode = str(settings.get("general_mode", "CHỈ LOGIN")).strip().upper()
    base = {"general_app": gen_app, "login_max": login_max_val, "general_method": gen_method}

    actions = []

    # 🟢 1. NẾU LÀ TIKTOK WHEE
    if "WHEE" in gen_app:
        if "REG" in mode:
            actions.append({"task": "REG_ACC", **base})
        else:
            actions.append({"task": "LOGIN", **base})

        if settings.get("whee_edit_name") or settings.get("whee_edit_bio") or settings.get("whee_edit_avatar"):
            actions.append({"task": "WHEE_EDIT_PROFILE", **base})
        if settings.get("whee_post_video_enable", True):
            actions.append({"task": "WHEE_POST", **base})
        actions.append({"task": "XOAY VÒNG", **base})
        return actions

    # 🟢 2. NẾU LÀ TIKTOK THƯỜNG HOẶC TIKTOK STUDIO
    post_item = next((it for it in script_list if _is_post_item(it)), None)
    post_details = post_item.get("details", {}) if post_item else DEFAULT_POST_DETAILS

    watch_item = next((it for it in script_list if is_watch_item(it)), None)
    watch_details = watch_item.get("details", {}) if watch_item else DEFAULT_WATCH_DETAILS

    # Khớp chuẩn 100% các chế độ chạy:
    if mode == "CHỈ LOGIN":
        actions.append({"task": "LOGIN", **base})

    elif mode == "CHỈ CHANGE":
        change = change_action(settings, **base)
        actions.append(change)

    elif mode == "LOGIN ➔ ĐĂNG VIDEO":
        actions.append({"task": "LOGIN", **base})  
        actions.append({"task": "ĐĂNG VIDEO", "details": post_details, **base})
        actions.append({"task": "XOAY VÒNG", **base})

    elif mode == "LOGIN ➔ XEM VIDEO":
        actions.append({"task": "LOGIN", **base})  
        actions.append({"task": "XEM VIDEO", "details": watch_details, **base})
        actions.append({"task": "XOAY VÒNG", **base})

    elif mode == "CHUYỂN ACC ➔ ĐĂNG VIDEO":
        actions.append({"task": "SWITHCH_POST", "details": post_details, **base})
        actions.append({"task": "ĐĂNG VIDEO", "details": post_details, **base})
        actions.append({"task": "XOAY VÒNG", **base})

    elif mode == "CHUYỂN ACC ➔ XEM VIDEO":
        actions.append({"task": "SWITHCH_VIEW", "details": watch_details, **base})
        actions.append({"task": "XEM VIDEO", "details": watch_details, **base})
        actions.append({"task": "XOAY VÒNG", **base})

    else:
        actions.append({"task": "LOGIN", **base})
        actions.append({"task": "XOAY VÒNG", **base})

    return actions


def save_config(config_data):
    """Cập nhật settings/script_list, biên dịch lại actions và ghi file nguyên tử."""
    try:
        current = load_config()
        if isinstance(config_data, dict):
            src_settings = config_data.get("settings")
            if isinstance(src_settings, dict):
                current["settings"].update(src_settings)
            if isinstance(config_data.get("script_list"), list):
                current["script_list"] = config_data["script_list"]
                
            if "campaigns" in config_data:
                current["campaigns"] = config_data["campaigns"]

        current["actions"] = compile_actions(current["settings"], current["script_list"])

        tmp = CONFIG_FILE + ".tmp"
        with _io_lock:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=4)
            os.replace(tmp, CONFIG_FILE)
        return current
    except Exception as e:
        print(f" [LỖI] Lưu file script_config.json thất bại: {e}")
        return None


def load_ai_keys():
    """Đọc Config/ai_keys.txt → {name: api_key}. Mỗi dòng: name|api_key."""
    keys = {}
    if not os.path.exists(AI_KEYS_FILE):
        return keys
    try:
        with _io_lock, open(AI_KEYS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "|" not in line:
                    continue
                name, key = line.split("|", 1)
                name = name.strip()
                if name:
                    keys[name] = key.strip()
    except Exception as e:
        print(f"Lỗi đọc ai_keys.txt: {e}")
    return keys


def save_ai_keys(keys):
    """Ghi {name: api_key} vào Config/ai_keys.txt (nguyên tử)."""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        lines = [f"{name}|{key}" for name, key in keys.items() if name]
        tmp = AI_KEYS_FILE + ".tmp"
        with _io_lock:
            with open(tmp, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            os.replace(tmp, AI_KEYS_FILE)
        return True
    except Exception as e:
        print(f" [LỖI] Lưu ai_keys.txt thất bại: {e}")
        return False

def parse_watch_links(text):
    """Phân tích danh sách link xem video từ chuỗi hoặc text box."""
    if not text:
        return []
    links = []
    for line in str(text).splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split("|")
            url = parts[0].strip()
            target_views = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1
            links.append((url, target_views))
    return links