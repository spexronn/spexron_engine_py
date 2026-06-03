# ==========================================
# SPEXRON ENGINE v2.0 - PROCESS PICKER DIALOG
# Cheat Engine tarzı süreç seçim penceresi
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
from ctypes import wintypes
from PIL import Image, ImageTk
from spexron_scanner import enumerate_processes

# ── Windows API DLLs ──
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
shell32 = ctypes.windll.shell32
kernel32 = ctypes.windll.kernel32

# ── Constants ──
SHGFI_ICON = 0x000000100
SHGFI_SMALLICON = 0x000000001
SHGFI_USEFILEATTRIBUTES = 0x000000010
FILE_ATTRIBUTE_NORMAL = 0x80
DIB_RGB_COLORS = 0

# ── Ctypes Structures ──
class SHFILEINFOW(ctypes.Structure):
    _fields_ = [
        ("hIcon", wintypes.HANDLE),
        ("iIcon", ctypes.c_int),
        ("dwAttributes", wintypes.DWORD),
        ("szDisplayName", ctypes.c_wchar * 260),
        ("szTypeName", ctypes.c_wchar * 80)
    ]

class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HANDLE),
        ("hbmColor", wintypes.HANDLE)
    ]

class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", ctypes.c_void_p)
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3)
    ]

# ── Set function signatures for 64-bit safety ──
# kernel32
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL
kernel32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL

# user32
user32.GetIconInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
user32.GetIconInfo.restype = wintypes.BOOL
user32.GetDC.argtypes = [wintypes.HWND]
user32.GetDC.restype = wintypes.HDC
user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
user32.ReleaseDC.restype = ctypes.c_int
user32.DestroyIcon.argtypes = [wintypes.HANDLE]
user32.DestroyIcon.restype = wintypes.BOOL

# gdi32
gdi32.GetObjectW.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p]
gdi32.GetObjectW.restype = ctypes.c_int
gdi32.GetDIBits.argtypes = [wintypes.HDC, wintypes.HANDLE, wintypes.UINT, wintypes.UINT, ctypes.c_void_p, ctypes.c_void_p, wintypes.UINT]
gdi32.GetDIBits.restype = ctypes.c_int
gdi32.DeleteObject.argtypes = [wintypes.HANDLE]
gdi32.DeleteObject.restype = wintypes.BOOL

# shell32
shell32.SHGetFileInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p, wintypes.UINT, wintypes.UINT]
shell32.SHGetFileInfoW.restype = ctypes.c_void_p




class ProcessPickerDialog(tk.Toplevel):
    def __init__(self, parent, callback, lang, localization, theme_palette=None):
        super().__init__(parent)
        self._loc  = localization
        self._lang = lang
        self._cb   = callback

        if theme_palette is None:
            # Fallback theme if not provided (Premium solid Dark Theme)
            theme_palette = {
                "bg":           "#121212",
                "surface":      "#1E1E1E",
                "surface2":     "#252525",
                "surface3":     "#2D2D2D",
                "border":       "#2D2D2D",
                "border_hi":    "#3B82F6",
                "text":         "#FFFFFF",
                "text2":        "#FFFFFF",
                "text_muted":   "#A3A3A3",
                "accent":       "#3B82F6",
                "accent_dim":   "#252525",
                "btn_primary":  "#3B82F6",
                "btn_primary_h":"#2563EB",
                "btn_default":  "#252525",
                "btn_default_h":"#2D2D2D",
                "entry_bg":     "#121212",
                "sb_thumb":       "#2D2D2D",
                "sb_thumb_hover": "#3B82F6",
                "sb_trough":      "#121212",
            }
        self._palette = theme_palette

        self.title(self.t("picker_title"))
        self.geometry("520x580")
        self.resizable(True, True)
        self.configure(bg=self._palette["bg"])
        self.transient(parent)
        self.grab_set()

        self._all  = enumerate_processes()
        self._show = self._all.copy()

        self._build()
        self._fill()
        self._center(parent)

    # ── Localization helper ───────────────────────────────────────────────────
    def t(self, key, *args):
        text = self._loc[self._lang].get(key, key)
        return text.format(*args) if args else text

    # ── Layout ───────────────────────────────────────────────────────────────
    def _build(self):
        p = self._palette

        # ── Title bar ──
        hdr = tk.Frame(self, bg=p["surface2"])
        hdr.pack(fill=tk.X)
        
        # Left blue accent line (unifying with other panels)
        div_acc = tk.Frame(hdr, bg=p["accent"], width=3)
        div_acc.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            hdr, text=self.t("picker_header"),
            font=("Segoe UI", 10, "bold"),
            fg=p["text"], bg=p["surface2"], pady=12
        ).pack(side=tk.LEFT, padx=12)

        tk.Label(
            hdr, text="Spexron Engine",
            font=("Segoe UI", 8, "bold"), fg=p["text_muted"], bg=p["surface2"]
        ).pack(side=tk.RIGHT, padx=15)

        # Separator line
        tk.Frame(self, bg=p["border"], height=1).pack(fill=tk.X)

        # ── Filter ──
        filt = tk.Frame(self, bg=p["bg"])
        filt.pack(fill=tk.X, padx=15, pady=(12, 6))
        tk.Label(
            filt, text=self.t("picker_filter"),
            font=("Segoe UI", 9, "bold"),
            fg=p["text"], bg=p["bg"]
        ).pack(side=tk.LEFT, padx=(0, 8))

        self._ent = tk.Entry(
            filt, bg=p["entry_bg"], fg=p["text"],
            insertbackground=p["accent"],
            font=("Segoe UI", 10),
            relief=tk.FLAT, highlightthickness=1,
            highlightbackground=p["border"], highlightcolor=p["accent"]
        )
        self._ent.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, ipadx=4)
        self._ent.bind("<KeyRelease>", self._on_filter)
        self._ent.focus_set()

        # ── Process list ──
        lst = tk.Frame(self, bg=p["bg"])
        lst.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        cols = ("PID",)
        self._tree = ttk.Treeview(lst, columns=cols, show="tree headings",
                                  style="Treeview")
        self._tree.heading("#0",   text=self.t("picker_col_name").upper(), anchor=tk.W)
        self._tree.heading("PID",  text=self.t("picker_col_pid").upper(), anchor=tk.W)
        self._tree.column("#0",    width=350, anchor=tk.W)
        self._tree.column("PID",   width=110, anchor=tk.W, stretch=False)

        vsb = ttk.Scrollbar(lst, orient=tk.VERTICAL, command=self._tree.yview, style="Modern.Vertical.TScrollbar")
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree.bind("<Double-1>",  self._on_select)
        self._tree.bind("<Return>",    self._on_select)

        # ── Count badge ──
        self._badge_frame = tk.Frame(self, bg=p["surface2"], padx=8, pady=2)
        self._badge_frame.pack(anchor=tk.W, padx=16, pady=4)
        
        self._lbl_count = tk.Label(
            self._badge_frame, text="", font=("Segoe UI", 8, "bold"),
            fg=p["accent"], bg=p["surface2"]
        )
        self._lbl_count.pack()

        # ── Buttons ──
        btn_row = tk.Frame(self, bg=p["bg"])
        btn_row.pack(fill=tk.X, padx=15, pady=(5, 15))

        def _btn(parent, text, bg, fg, cmd, style_type="default"):
            active_bg = p["btn_default_h"] if style_type == "default" else p["btn_primary_h"]
            b = tk.Button(
                parent, text=text, bg=bg, fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT, cursor="hand2",
                command=cmd, bd=1,
                highlightbackground=p["border"] if style_type == "default" else bg,
                highlightthickness=1
            )
            b.pack(side=tk.LEFT if style_type == "default" else tk.RIGHT,
                   padx=4, ipady=5, ipadx=12)
            return b

        _btn(btn_row, self.t("picker_btn_refresh"), p["btn_default"], p["text"], self._refresh, "default")
        _btn(btn_row, self.t("picker_btn_cancel"),  p["btn_default"], p["text"], self.destroy, "default")
        _btn(btn_row, self.t("picker_btn_attach"),  p["btn_primary"], p["surface"], self._on_select, "primary")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _fill(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        p = self._palette
        for pid, name in self._show:
            icon_img = self._get_cached_icon(pid)
            self._tree.insert("", tk.END, text=name, values=(pid,), image=icon_img)
        self._lbl_count.config(text=self.t("picker_lbl_count", len(self._show)))


    def _on_filter(self, _event=None):
        q = self._ent.get().strip().lower()
        self._show = [
            (p, n) for p, n in self._all
            if q in n.lower() or q in str(p)
        ] if q else self._all.copy()
        self._fill()

    def _refresh(self):
        self._all  = enumerate_processes()
        self._on_filter()

    def _on_select(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Spexron", self.t("picker_warning"), parent=self)
            return
        name = self._tree.item(sel[0], "text")
        pid_str = self._tree.item(sel[0], "values")[0]
        self._cb(int(pid_str), name)
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width()  - w) // 2
        y = parent.winfo_y() + (parent.winfo_height() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ── Icon extraction and caching helpers ──────────────────────────────────
    def _hicon_to_pil(self, hIcon):
        if not hIcon:
            return None
        
        iconinfo = ICONINFO()
        if not user32.GetIconInfo(hIcon, ctypes.byref(iconinfo)):
            return None
        
        hbmColor = iconinfo.hbmColor
        hbmMask = iconinfo.hbmMask
        
        bmp = BITMAP()
        if not gdi32.GetObjectW(hbmColor, ctypes.sizeof(bmp), ctypes.byref(bmp)):
            if hbmColor: gdi32.DeleteObject(hbmColor)
            if hbmMask: gdi32.DeleteObject(hbmMask)
            return None
        
        width = bmp.bmWidth
        height = bmp.bmHeight
        
        hdc = user32.GetDC(0)
        
        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        bmi.bmiHeader.biSizeImage = width * height * 4
        
        buf = ctypes.create_string_buffer(width * height * 4)
        copied = gdi32.GetDIBits(hdc, hbmColor, 0, height, buf, ctypes.byref(bmi), DIB_RGB_COLORS)
        
        user32.ReleaseDC(0, hdc)
        
        if hbmColor: gdi32.DeleteObject(hbmColor)
        if hbmMask: gdi32.DeleteObject(hbmMask)
        
        if not copied:
            return None
            
        img = Image.frombytes("RGBA", (width, height), buf.raw, "raw", "BGRA")
        
        # Verify transparency
        has_alpha = False
        pixels = img.split()
        if len(pixels) == 4:
            alpha = pixels[3]
            extrema = alpha.getextrema()
            if extrema[1] > 0:
                has_alpha = True
                
        if not has_alpha:
            img = img.convert("RGB").convert("RGBA")
            
        return img

    def _get_process_path(self, pid):
        h_process = kernel32.OpenProcess(0x1000, False, pid)
        if not h_process:
            h_process = kernel32.OpenProcess(0x0400, False, pid)
        if not h_process:
            return None
        
        size = wintypes.DWORD(260)
        buf = ctypes.create_unicode_buffer(size.value)
        
        success = False
        if hasattr(kernel32, "QueryFullProcessImageNameW"):
            success = kernel32.QueryFullProcessImageNameW(h_process, 0, buf, ctypes.byref(size))
        
        kernel32.CloseHandle(h_process)
        
        if success:
            return buf.value
        return None

    def _get_file_icon(self, file_path):
        shfi = SHFILEINFOW()
        res = shell32.SHGetFileInfoW(
            file_path,
            0,
            ctypes.byref(shfi),
            ctypes.sizeof(shfi),
            SHGFI_ICON | SHGFI_SMALLICON
        )
        if not res or not shfi.hIcon:
            return None
        
        img = self._hicon_to_pil(shfi.hIcon)
        user32.DestroyIcon(shfi.hIcon)
        return img

    def _get_default_icon(self):
        shfi = SHFILEINFOW()
        res = shell32.SHGetFileInfoW(
            "dummy.exe",
            FILE_ATTRIBUTE_NORMAL,
            ctypes.byref(shfi),
            ctypes.sizeof(shfi),
            SHGFI_ICON | SHGFI_SMALLICON | SHGFI_USEFILEATTRIBUTES
        )
        if not res or not shfi.hIcon:
            return None
        img = self._hicon_to_pil(shfi.hIcon)
        user32.DestroyIcon(shfi.hIcon)
        return img

    def _get_cached_icon(self, pid):
        if not hasattr(self, "_icon_cache"):
            self._icon_cache = {}
            
        if pid in self._icon_cache:
            return self._icon_cache[pid]
            
        img = None
        try:
            path = self._get_process_path(pid)
            if path:
                img = self._get_file_icon(path)
        except Exception:
            pass
            
        if not img:
            img = self._get_default_icon()
            
        if img:
            if img.size != (16, 16):
                img = img.resize((16, 16), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._icon_cache[pid] = photo
            return photo
            
        return ""

