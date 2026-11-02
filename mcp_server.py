"""Máy chủ MCP cho Auto Studio: cho Claude Code xem và điều khiển các máy qua cổng nội bộ 127.0.0.1.

Cần mở Auto Studio và bật "Cổng điều khiển" trước. Token đọc từ Config/control_token.txt.
Thêm vào Claude Code:  claude mcp add autostudio -- <đường dẫn venv>\\Scripts\\python.exe mcp_server.py
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import Image, MCPServer
from mcp.server.mcpserver.exceptions import ToolError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "Config", "control_token.txt")
CONFIG_FILE = os.path.join(BASE_DIR, "Config", "script_config.json")


def _port():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return int(json.load(f).get("settings", {}).get("control_port", 8765))
    except (OSError, ValueError, TypeError):
        return 8765


def _call(method, path, body=None):
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
    except OSError:
        raise ToolError("Chưa có token — hãy mở Auto Studio và bật Cổng điều khiển.")
    data = json.dumps(body or {}).encode("utf-8") if method == "POST" else None
    req = urllib.request.Request(f"http://127.0.0.1:{_port()}{path}", data=data, method=method,
                                 headers={"X-Token": token, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as res:
            raw = res.read()
            return raw if res.headers.get_content_type() == "image/png" else json.loads(raw)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("error", str(e))
        except ValueError:
            msg = str(e)
        raise ToolError(msg)
    except urllib.error.URLError:
        raise ToolError("Không kết nối được Auto Studio — app chưa mở hoặc cổng điều khiển đang tắt.")


mcp = MCPServer("autostudio", instructions="Điều khiển app Auto Studio (TikTok trên điện thoại Android qua ADB).")


@mcp.tool()
def list_devices() -> dict:
    """Danh sách máy, trạng thái, tài khoản đang chạy và thống kê."""
    return _call("GET", "/devices")


@mcp.tool()
def get_logs(serial: str = "", limit: int = 50) -> dict:
    """Nhật ký gần nhất của một máy (serial) hoặc tất cả máy (để trống)."""
    return _call("GET", f"/logs?serial={urllib.parse.quote(serial)}&limit={int(limit)}")


@mcp.tool()
def run_task(task: str = "PIPELINE", serials: list[str] | None = None) -> dict:
    """Chạy tác vụ trên các máy. task: PIPELINE | LOGIN | POST_VIDEO | CHANGE. serials trống = tất cả máy."""
    return _call("POST", "/run", {"task": task.upper(), "serials": serials or "all"})


@mcp.tool()
def stop(serials: list[str] | None = None) -> dict:
    """Dừng các máy đang chạy. serials trống = dừng tất cả."""
    return _call("POST", "/stop", {"serials": serials or "all"})


@mcp.tool()
def set_paused(paused: bool = True) -> dict:
    """Tạm dừng (True) hoặc tiếp tục (False) tất cả máy."""
    return _call("POST", "/pause", {"paused": paused})


@mcp.tool()
def screenshot(serial: str) -> Image:
    """Chụp màn hình một máy."""
    return Image(data=_call("GET", f"/screenshot?serial={urllib.parse.quote(serial)}"), format="png")


@mcp.tool()
def tap(serial: str, x: int, y: int) -> dict:
    """Chạm vào tọa độ (x, y) trên máy."""
    return _call("POST", "/tap", {"serial": serial, "x": x, "y": y})


@mcp.tool()
def swipe(serial: str, x1: int, y1: int, x2: int, y2: int, ms: int = 300) -> dict:
    """Vuốt từ (x1, y1) tới (x2, y2)."""
    return _call("POST", "/swipe", {"serial": serial, "x1": x1, "y1": y1, "x2": x2, "y2": y2, "ms": ms})


@mcp.tool()
def type_text(serial: str, text: str) -> dict:
    """Gõ chữ không dấu (ASCII) vào ô đang chọn."""
    return _call("POST", "/text", {"serial": serial, "text": text})


@mcp.tool()
def press_key(serial: str, key: str) -> dict:
    """Bấm phím: HOME, BACK, APP_SWITCH, ENTER, POWER, VOLUME_UP, VOLUME_DOWN, DEL."""
    return _call("POST", "/key", {"serial": serial, "key": key})


@mcp.tool()
def restart_app(serial: str) -> dict:
    """Tắt và mở lại app TikTok đang cấu hình trên máy."""
    return _call("POST", "/restart_app", {"serial": serial})


if __name__ == "__main__":
    mcp.run("stdio")
