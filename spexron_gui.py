# ==========================================
# SPEXRON ENGINE v2.0 - MODERN GUI
# GitHub Dark / Linear tarzı clean modern UI
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import os

from spexron_localization import LOCALIZATION
from spexron_scanner import MemoryScanner
from spexron_processpicker import ProcessPickerDialog

# ─────────────────────────────────────────────────────────────────────────────
# RENK PALETİ  — Modern GitHub Dark / Slate teması
# ─────────────────────────────────────────────────────────────────────────────
THEME_LIGHT = {
    "bg":           "#121212",   # Deep premium dark background
    "surface":      "#1E1E1E",   # Pure premium solid charcoal panel background (exact visual color!)
    "surface2":     "#252525",   # Gray elevated panel / header
    "surface3":     "#2D2D2D",   # Hover state
    "border":       "#2D2D2D",   # Clean slate border
    "border_hi":    "#3B82F6",   # Focus border (Accent Fluent Blue)
    "border_sub":   "#1E1E1E",   # Sub-border to separate rows cleanly
    "text":         "#FFFFFF",   # Pure white for absolute clarity
    "text2":        "#FFFFFF",   # Pure white secondary text
    "text_muted":   "#A3A3A3",   # Muted light grey text
    "text_code":    "#FFFFFF",
    "accent":       "#3B82F6",   # Fluent Blue Accent
    "accent_dim":   "#252525",   # Soft blue tint
    "accent_hover": "#2D2D2D",
    "gold":         "#F59E0B",
    "gold_dim":     "#2E251B",
    "green":        "#22C55E",   # Success green
    "green_dim":    "#153723",
    "red":          "#EF4444",   # Danger red
    "red_dim":      "#3B1B1E",
    "cyan":         "#06B6D4",
    "toolbar_bg":   "#1E1E1E",
    "statusbar_bg": "#1E1E1E",
    "btn_primary":  "#3B82F6",   # Accent Blue primary button
    "btn_primary_h":"#2563EB",   # Hover primary button
    "btn_default":  "#252525",   # Dark grey default button
    "btn_default_h":"#2D2D2D",   # Hover default button
    "btn_danger":   "#EF4444",
    "btn_danger_h": "#DC2626",
    "entry_bg":     "#121212",
    "entry_border": "#2D2D2D",
    "sel_found":    "#2D2D2D",
    "sel_found_fg": "#FFFFFF",
    "sel_cheat":    "#2D2D2D",
    "sel_cheat_fg": "#FFFFFF",
    "locked_row":   "#3B82F6",
    "progress_bg":  "#252525",
    "progress_fill":"#3B82F6",
    "sb_thumb":       "#2D2D2D",   # Custom scrollbar thumb
    "sb_thumb_hover": "#3B82F6",   # Custom scrollbar hover accent
    "sb_trough":      "#121212",   # Custom scrollbar trough
    "sky_blue":       "#38bdf8",   # Sky blue accent for dark mode
}

THEME_DARK = THEME_LIGHT.copy()
C = THEME_LIGHT.copy()


# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI
# ─────────────────────────────────────────────────────────────────────────────
def _build_scan_map(loc, lang):
    L  = loc[lang]
    ST = MemoryScanner
    return {
        L["scan_exact"]:     ST.ST_EXACT,
        L["scan_bigger"]:    ST.ST_BIGGER,
        L["scan_smaller"]:   ST.ST_SMALLER,
        L["scan_between"]:   ST.ST_BETWEEN,
        L["scan_unknown"]:   ST.ST_UNKNOWN,
        L["scan_increased"]: ST.ST_INCREASED,
        L["scan_decreased"]: ST.ST_DECREASED,
        L["scan_changed"]:   ST.ST_CHANGED,
        L["scan_unchanged"]: ST.ST_UNCHANGED,
    }


def _build_val_type_map(loc, lang):
    L = loc[lang]
    return {
        L["val_1byte"]: "1 Byte",
        L["val_2bytes"]: "2 Bytes",
        L["val_4bytes"]: "4 Bytes",
        L["val_8bytes"]: "8 Bytes",
        L["val_float"]: "Float",
        L["val_double"]: "Double",
    }


# ─────────────────────────────────────────────────────────────────────────────
# ÖZEL BİLEŞENLER
# ─────────────────────────────────────────────────────────────────────────────

class ModernButton(tk.Frame):
    """Modern düz flat buton — Shadcn/Vercel 2026 tasarımı."""

    STYLES = {
        "primary": {
            "bg":       C["btn_primary"],
            "bg_hover": C["btn_primary_h"],
            "fg":       "#FAFAFA",
            "border":   C["btn_primary"],
        },
        "default": {
            "bg":       C["btn_default"],
            "bg_hover": C["btn_default_h"],
            "fg":       C["text2"],
            "border":   C["border"],
        },
        "accent": {
            "bg":       C["accent_dim"],
            "bg_hover": C["surface3"],
            "fg":       C["text"],
            "border":   C["border"],
        },
        "danger": {
            "bg":       C["btn_danger"],
            "bg_hover": C["btn_danger_h"],
            "fg":       "#FAFAFA",
            "border":   C["btn_danger"],
        },
    }

    def __init__(self, parent, text="", command=None,
                 style="default", font_size=9, label_padx=12, label_pady=8, **kwargs):
        self._style = style
        st = self.STYLES.get(style, self.STYLES["default"])
        self._bg       = st["bg"]
        self._bg_h     = st["bg_hover"]
        self._fg       = st["fg"]
        self._border   = st["border"]
        self._cmd      = command
        self._enabled  = True

        super().__init__(parent, bg=self._border, padx=1, pady=1,
                         cursor="hand2", **kwargs)

        self._inner = tk.Frame(self, bg=self._bg)
        self._inner.pack(fill=tk.BOTH, expand=True)

        self._lbl = tk.Label(
            self._inner, text=text,
            bg=self._bg, fg=self._fg,
            font=("Segoe UI", font_size, "bold"),
            padx=label_padx, pady=label_pady
        )
        self._lbl.pack(fill=tk.BOTH, expand=True)

        for w in (self, self._inner, self._lbl):
            w.bind("<Enter>",    self._enter)
            w.bind("<Leave>",    self._leave)
            w.bind("<Button-1>", self._click)

    def _enter(self, _=None):
        if not self._enabled:
            return
        self._inner.config(bg=self._bg_h)
        self._lbl.config(bg=self._bg_h)

    def _leave(self, _=None):
        if not self._enabled:
            return
        self._inner.config(bg=self._bg)
        self._lbl.config(bg=self._bg)

    def _click(self, _=None):
        if self._enabled and self._cmd:
            self._cmd()

    def set_text(self, text):
        self._lbl.config(text=text)

    def enable(self):
        self._enabled = True
        self._lbl.config(fg=self._fg)
        self.config(cursor="hand2")

    def disable(self):
        self._enabled = False
        self._lbl.config(fg=C["text_muted"])
        self.config(cursor="")
        self._inner.config(bg=self._bg)
        self._lbl.config(bg=self._bg)

    def retheme(self):
        self.STYLES = {
            "primary": {
                "bg":       C["btn_primary"],
                "bg_hover": C["btn_primary_h"],
                "fg":       "#FFFFFF",
                "border":   C["btn_primary"],
            },
            "default": {
                "bg":       C["btn_default"],
                "bg_hover": C["btn_default_h"],
                "fg":       C["text2"],
                "border":   C["border"],
            },
            "accent": {
                "bg":       C["accent_dim"],
                "bg_hover": C["surface3"],
                "fg":       C["text"],
                "border":   C["border"],
            },
            "danger": {
                "bg":       C["btn_danger"],
                "bg_hover": C["btn_danger_h"],
                "fg":       "#FAFAFA",
                "border":   C["btn_danger"],
            },
        }
        st = self.STYLES.get(self._style, self.STYLES["default"])
        self._bg       = st["bg"]
        self._bg_h     = st["bg_hover"]
        self._fg       = st["fg"]
        self._border   = st["border"]

        self.config(bg=self._border)
        self._inner.config(bg=self._bg)
        self._lbl.config(bg=self._bg, fg=self._fg)


class Badge(tk.Label):
    """Pill/badge — modern minimal durum göstergesi."""
    def __init__(self, parent, text="", preset="muted", **kwargs):
        self._preset = preset
        super().__init__(parent, text=f" {text} ",
                          font=("Segoe UI", 8, "bold"),
                          padx=6, pady=2, **kwargs)
        self.retheme()

    def update_preset(self, text, preset="muted"):
        self._preset = preset
        self.config(text=f" {text} ")
        self.retheme()

    def retheme(self):
        presets = {
            "green":  (C["green_dim"],  C["green"]),
            "red":    (C["red_dim"],    C["red"]),
            "gold":   (C["gold_dim"],   C["gold"]),
            "accent": (C["accent_dim"], C["accent"]),
            "muted":  (C["surface3"],   C["text_muted"]),
        }
        bg, fg = presets.get(self._preset, presets["muted"])
        self.config(bg=bg, fg=fg)


class SidebarTab(tk.Frame):
    """ VS Code / Obsidian tarzı modern düz flat sidebar sekme butonu. """
    def __init__(self, parent, text, command, active=False):
        super().__init__(parent, bg=C["surface2"], cursor="hand2")
        self._text = text
        self._cmd = command
        self._active = active
        
        self._lbl = tk.Label(self, text=text, bg=C["surface2"], fg=C["text2"],
                             font=("Segoe UI", 9, "bold"), anchor=tk.W, padx=16, pady=10)
        self._lbl.pack(fill=tk.BOTH, expand=True)
        
        for w in (self, self._lbl):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._on_click)
            
        self.update_state(active)
        
    def _on_enter(self, _=None):
        if not self._active:
            self.config(bg=C["surface3"])
            self._lbl.config(bg=C["surface3"])
            
    def _on_leave(self, _=None):
        if not self._active:
            self.config(bg=C["surface2"])
            self._lbl.config(bg=C["surface2"])
            
    def _on_click(self, _=None):
        self._cmd()
        
    def update_state(self, active):
        self._active = active
        if active:
            self.config(bg=C["accent_dim"])
            self._lbl.config(bg=C["accent_dim"], fg=C["accent"])
        else:
            self.config(bg=C["surface2"])
            self._lbl.config(bg=C["surface2"], fg=C["text2"])

    def retheme(self):
        self.update_state(self._active)


class AutoScrollbar(ttk.Scrollbar):
    """Sadece içeriğin ekrana sığmadığı durumlarda görünen dinamik scrollbar."""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
        else:
            self.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Scrollbar.set(self, lo, hi)


class SectionCard(tk.Frame):
    """Modern minimalist flat card container."""
    def __init__(self, parent, title="", accent=None, **kwargs):
        super().__init__(parent, bg=C["border"], padx=1, pady=1, **kwargs)
        self._title = title
        self._accent = accent
        self._inner = tk.Frame(self, bg=C["surface"])
        self._inner.pack(fill=tk.BOTH, expand=True)
        self._hdr = None
        self._lbl = None
        self._acc_bar = None

        if title:
            self._hdr = tk.Frame(self._inner, bg=C["surface2"])
            self._hdr.pack(fill=tk.X)
            if accent:
                self._acc_bar = tk.Frame(self._hdr, bg=accent, width=2)
                self._acc_bar.pack(side=tk.LEFT, fill=tk.Y)
            self._lbl = tk.Label(
                self._hdr, text=f"  {title.upper()}",
                bg=C["surface2"], fg=C["text_muted"],
                font=("Segoe UI", 8, "bold"),
                pady=8, anchor=tk.W
            )
            self._lbl.pack(side=tk.LEFT, fill=tk.X)
            self._div = tk.Frame(self._inner, bg=C["border"], height=1)
            self._div.pack(fill=tk.X)

    @property
    def body(self):
        return self._inner

    def retheme(self):
        self.config(bg=C["border"])
        self._inner.config(bg=C["surface"])
        if self._title:
            self._hdr.config(bg=C["surface2"])
            self._lbl.config(bg=C["surface2"], fg=C["text_muted"])
            self._div.config(bg=C["border"])


class ModernEntry(tk.Frame):
    """Shadcn/Vercel style Entry with high contrast Zinc focus border."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=C["border"], padx=1, pady=1)
        self._entry = tk.Entry(
            self, bg=C["entry_bg"], fg=C["text"],
            insertbackground=C["accent"],
            font=("Consolas", 11),
            relief=tk.FLAT,
            **kwargs
        )
        self._entry.pack(fill=tk.X, ipady=6, padx=6)
        self._entry.bind("<FocusIn>",  lambda _: self.config(bg=C["border_hi"]))
        self._entry.bind("<FocusOut>", lambda _: self.config(bg=C["border"]))

    def get(self):
        return self._entry.get()

    def delete(self, *a):
        return self._entry.delete(*a)

    def insert(self, *a):
        return self._entry.insert(*a)

    def config_entry(self, **kw):
        return self._entry.config(**kw)

    def bind_entry(self, *a, **kw):
        return self._entry.bind(*a, **kw)

    def retheme(self):
        self.config(bg=C["border"])
        self._entry.config(bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"])


class ModernCombo(tk.Frame):
    """Custom flat combobox replacement using a flat button and context menu."""
    def __init__(self, parent, values=None, state="readonly", width=None, **kwargs):
        # Strip out ttk Combobox specific options
        kwargs.pop("orient", None)
        kwargs.pop("mode", None)
        kwargs.pop("style", None)
        state = kwargs.pop("state", None)
        values = kwargs.pop("values", None)
        
        super().__init__(parent, bg=C["border"], padx=1, pady=1)
        self.values = values or []
        self._selected_value = ""
        self._bindings = {}

        # Inner frame to hold the label and provide hover feedback
        self._inner = tk.Frame(self, bg=C["surface2"], cursor="hand2")
        self._inner.pack(fill=tk.BOTH, expand=True)

        lbl_kwargs = {
            "bg": C["surface2"],
            "fg": C["text2"],
            "font": ("Segoe UI", 9, "bold"),
            "anchor": tk.CENTER,
            "padx": 10,
            "pady": 5
        }
        if width is not None:
            lbl_kwargs["width"] = width

        self._lbl = tk.Label(self._inner, text="", **lbl_kwargs)
        self._lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.theme_bg = "border"

        for w in (self, self._inner, self._lbl):
            w.bind("<Enter>",    self._on_enter)
            w.bind("<Leave>",    self._on_leave)
            w.bind("<Button-1>", self._on_click)

    def _on_enter(self, _=None):
        self._inner.config(bg=C["surface3"])
        self._lbl.config(bg=C["surface3"], fg=C["accent"])

    def _on_leave(self, _=None):
        self._inner.config(bg=C["surface2"])
        self._lbl.config(bg=C["surface2"], fg=C["text2"])

    def _on_click(self, event):
        gui = self._gui_ref()
        
        # Check if the active menu belongs to this combobox
        if hasattr(gui, "active_menu") and gui.active_menu:
            old_menu = gui.active_menu
            is_same_owner = getattr(old_menu, "owner", None) == self
            try:
                old_menu.destroy()
            except Exception:
                pass
            if is_same_owner:
                return
        
        top = self.winfo_toplevel()
        menu = ModernContextMenu(gui, parent=top)
        menu.owner = self
        for val in self.values:
            menu.add_command(val, command=lambda v=val: self._select(v))
        
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        menu.tk_popup(x, y)

    def _gui_ref(self):
        curr = self
        while curr:
            if hasattr(curr, "root"):
                return curr
            curr = curr.master
        return self.master

    def _select(self, value):
        self.set(value)
        if "<<ComboboxSelected>>" in self._bindings:
            for cb in self._bindings["<<ComboboxSelected>>"]:
                try:
                    cb(None)
                except Exception:
                    pass

    def get(self):
        return self._selected_value

    def set(self, value):
        self._selected_value = value
        self._lbl.config(text=f"{value}  ▾")

    def current(self, new_index=None):
        if new_index is None:
            try:
                return self.values.index(self._selected_value)
            except ValueError:
                return -1
        else:
            if 0 <= new_index < len(self.values):
                self.set(self.values[new_index])

    def bind(self, event, callback, add=None):
        if event not in self._bindings:
            self._bindings[event] = []
        self._bindings[event].append(callback)

    def configure(self, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        args = {**cnf, **kw}
        if "values" in args:
            self.values = args["values"]
            del args["values"]
        if "state" in args:
            del args["state"]
        if args:
            super().configure(**args)

    def config(self, cnf=None, **kw):
        self.configure(cnf, **kw)

    def retheme(self):
        self.config(bg=C["border"])
        self._inner.config(bg=C["surface2"])
        self._lbl.config(bg=C["surface2"], fg=C["text2"])


class ModernProgressBar(tk.Canvas):
    def __init__(self, parent, bg=None, fill_color=None, height=4, **kwargs):
        # Strip out ttk-specific options to prevent TclErrors
        kwargs.pop("orient", None)
        kwargs.pop("mode", None)
        
        self._bg = bg or C["progress_bg"]
        self._fill = fill_color or C["progress_fill"]
        self._value = 0
        
        super().__init__(parent, bg=self._bg, height=height, 
                         highlightthickness=0, bd=0, relief="flat", **kwargs)
        self.bind("<Configure>", lambda _: self._draw())

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1:
            return
        # Draw background trough
        self.create_rectangle(0, 0, w, h, fill=self._bg, outline="")
        # Draw progress bar fill
        fill_width = int(w * (self._value / 100.0))
        if fill_width > 0:
            self.create_rectangle(0, 0, fill_width, h, fill=self._fill, outline="")

    def __setitem__(self, key, value):
        if key == "value":
            self._value = max(0, min(100, float(value)))
            self._draw()
        else:
            super().__setitem__(key, value)

    def configure(self, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        args = {**cnf, **kw}
        if "value" in args:
            self._value = max(0, min(100, float(args["value"])))
            self._draw()
            del args["value"]
        if args:
            super().configure(**args)

    def config(self, cnf=None, **kw):
        self.configure(cnf, **kw)

    def retheme(self):
        self._bg = C["progress_bg"]
        self._fill = C["progress_fill"]
        self.config(bg=self._bg)
        self._draw()


class ModernSlider(tk.Canvas):
    """Custom premium flat themed slider replacement for standard Scale."""
    def __init__(self, parent, from_=0.0, to=100.0, command=None, **kwargs):
        self.from_ = float(from_)
        self.to = float(to)
        self.command = command
        self.value = self.from_
        self._hover = False
        
        # Colors
        self.bg = C["surface"]
        self.track_color = C["border"]
        self.fill_color = C["accent"]
        self.thumb_color = C["text"]
        self.thumb_hover_color = C["accent"]
        
        super().__init__(parent, bg=self.bg, height=18, highlightthickness=0, bd=0, cursor="hand2", **kwargs)
        
        self.bind("<Configure>", lambda _: self._draw())
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, _):
        self._hover = True
        self._draw()
        
    def _on_leave(self, _):
        self._hover = False
        self._draw()
        
    def _on_click(self, event):
        self._update_val(event.x)
        
    def _on_drag(self, event):
        self._update_val(event.x)
        
    def _update_val(self, x):
        w = self.winfo_width()
        if w <= 16:
            return
        padx = 8
        usable_w = w - 2 * padx
        pct = (x - padx) / usable_w
        pct = max(0.0, min(1.0, pct))
        self.value = self.from_ + pct * (self.to - self.from_)
        self._draw()
        if self.command:
            self.command(self.value)
            
    def set(self, val):
        try:
            val = float(val)
            self.value = max(self.from_, min(self.to, val))
            self._draw()
        except Exception:
            pass
        
    def get(self):
        return self.value
        
    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 16:
            return
            
        padx = 8
        usable_w = w - 2 * padx
        cy = h / 2
        
        # Calculate thumb X position
        pct = (self.value - self.from_) / (self.to - self.from_) if self.to != self.from_ else 0.0
        tx = padx + pct * usable_w
        
        # Draw track (rounded line)
        track_h = 4
        self.create_line(padx, cy, w - padx, cy, fill=self.track_color, width=track_h, capstyle="round")
        
        # Draw active track fill
        if tx > padx:
            self.create_line(padx, cy, tx, cy, fill=self.fill_color, width=track_h, capstyle="round")
            
        # Draw thumb (smooth round circle)
        thumb_r = 5 if not self._hover else 7
        color = self.thumb_hover_color if self._hover else self.thumb_color
        self.create_oval(tx - thumb_r, cy - thumb_r, tx + thumb_r, cy + thumb_r, fill=color, outline="")

    def retheme(self):
        self.bg = C["surface"]
        self.track_color = C["border"]
        self.fill_color = C["accent"]
        self.thumb_color = C["text"]
        self.thumb_hover_color = C["accent"]
        self.config(bg=self.bg)
        self._draw()



# ─────────────────────────────────────────────────────────────────────────────
# DEĞER DÜZENLEME DİYALOĞU
# ─────────────────────────────────────────────────────────────────────────────
class ValueEditorDialog(tk.Toplevel):
    def __init__(self, gui, addr, info):
        super().__init__(gui.root)
        self._gui  = gui
        self._addr = addr
        self._info = info

        # Seçili tüm kayıtların adreslerini topla (Çoklu Seçim Desteği)
        self._selected_items = gui.tree_saved.selection()
        self._selected_addrs = []
        for item in self._selected_items:
            vals = gui.tree_saved.item(item, "values")
            if vals:
                self._selected_addrs.append(vals[2])

        if addr not in self._selected_addrs:
            self._selected_addrs.append(addr)

        title_text = f"{gui.t('val_dialog_title')} ({len(self._selected_addrs)} {gui.t('lbl_entries_count').strip()})"
        self.title(f"{title_text} — Spexron Engine")
        self.geometry("440x360")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self.transient(gui.root)
        self.grab_set()
        self._build()
        self._center()

    def _build(self):
        g, addr, info = self._gui, self._addr, self._info

        # Header
        hdr = tk.Frame(self, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        tk.Frame(hdr, bg=C["accent"], width=3).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(hdr, text=f"  ✎  {g.t('val_dialog_title')}",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 11, "bold"), pady=12
                 ).pack(side=tk.LEFT)
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)
        body.columnconfigure(1, weight=1)

        # Info satırları
        cur_val = info["value"]
        if len(self._selected_addrs) > 1:
            addr_display = f"{len(self._selected_addrs)} {g.t('lbl_entries_count').strip()}"
            type_display = "Çoklu Tip (Multi)" if g.current_lang == "tr" else "Multi Type"
            cur_val = "—"
        else:
            addr_display = addr
            type_display = info["type"]
            if g.scanner:
                try:
                    v = g.scanner.read_memory(int(addr, 16), info["type"])
                    if v is not None:
                        cur_val = v
                except Exception:
                    pass

        for row, (lbl, val, fg) in enumerate([
            (g.t("lbl_dialog_addr"), addr_display,           C["accent"]),
            (g.t("lbl_dialog_type"), type_display,   C["text2"]),
            (g.t("lbl_dialog_current"), str(cur_val),   C["gold"]),
        ]):
            tk.Label(body, text=lbl, bg=C["bg"], fg=C["text_muted"],
                     font=("Segoe UI", 9)).grid(row=row, column=0, sticky=tk.W, pady=3)
            tk.Label(body, text=val, bg=C["bg"], fg=fg,
                     font=("Consolas", 10, "bold")).grid(
                     row=row, column=1, sticky=tk.W, padx=(12,0), pady=3)

        tk.Frame(body, bg=C["border"], height=1).grid(
            row=3, column=0, columnspan=2, sticky=tk.EW, pady=12)

        tk.Label(body, text=g.t("set_val_prompt", ""),
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 9, "bold")).grid(
                 row=4, column=0, columnspan=2, sticky=tk.W, pady=(0,4))

        self._ent_frame = tk.Frame(body, bg=C["accent"], padx=1, pady=1)
        self._ent_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW)
        self._ent = tk.Entry(self._ent_frame,
                             bg=C["entry_bg"], fg=C["text"],
                             insertbackground=C["accent"],
                             font=("Consolas", 13), relief=tk.FLAT)
        self._ent.pack(fill=tk.X, ipady=8)
        self._ent.insert(0, str(info["value"]))
        self._ent.select_range(0, tk.END)
        self._ent.focus_set()

        self._freeze_var = tk.BooleanVar(value=info["locked"])
        tk.Checkbutton(body, text=f"  {g.t('ctx_freeze')}",
                       variable=self._freeze_var,
                       bg=C["bg"], fg=C["text2"],
                       selectcolor=C["surface2"],
                       activebackground=C["bg"],
                       activeforeground=C["accent"],
                       font=("Segoe UI", 9)
                       ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(14,0))

        # Buttons
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)
        btn_row = tk.Frame(self, bg=C["surface"])
        btn_row.pack(fill=tk.X, padx=18, pady=12)

        ModernButton(btn_row, text=g.t("ctx_set_value"),
                     style="default", command=self._write_once
                     ).pack(side=tk.LEFT, ipady=0)

        ModernButton(btn_row, text=f"✔  {g.t('ctx_change_value')}",
                     style="primary", command=self._apply
                     ).pack(side=tk.RIGHT)

        self.bind("<Return>",  lambda _: self._apply())
        self.bind("<Escape>",  lambda _: self.destroy())

    def _apply(self):
        val = self._ent.get().strip()
        if not val:
            return
        g = self._gui
        locked = self._freeze_var.get()
        success_count = 0
        total_count = len(self._selected_addrs)

        for addr in self._selected_addrs:
            if addr in g.saved_cheats:
                info = g.saved_cheats[addr]
                g.saved_cheats[addr]["value"]  = val
                g.saved_cheats[addr]["locked"] = locked
                if g.scanner:
                    try:
                        target_addr = g._resolve_pointer(addr) if "->" in addr else int(addr, 16)
                        if target_addr is not None:
                            ok = g.scanner.write_memory(target_addr, val, info["type"])
                            if ok:
                                success_count += 1
                    except Exception:
                        pass

        if total_count > 1:
            g.log(g.t("log_records_frozen_multi", success_count, "✔" if locked else "—"), C["gold"])
        else:
            g.log(g.t("log_writeprocessmemory", self._addr, val), C["green"] if success_count > 0 else C["red"])

        g._refresh_cheat_tree()
        self.destroy()

    def _write_once(self):
        val = self._ent.get().strip()
        if not val:
            return
        g = self._gui
        success_count = 0

        for addr in self._selected_addrs:
            if addr in g.saved_cheats:
                info = g.saved_cheats[addr]
                g.saved_cheats[addr]["value"] = val
                if g.scanner:
                    try:
                        target_addr = g._resolve_pointer(addr) if "->" in addr else int(addr, 16)
                        if target_addr is not None:
                            ok = g.scanner.write_memory(target_addr, val, info["type"])
                            if ok:
                                success_count += 1
                    except Exception:
                        pass

        if len(self._selected_addrs) > 1:
            g.log(f"{success_count} adet adrese toplu deger yazildi.", C["gold"])
        else:
            g.log(g.t("log_writeprocessmemory", self._addr, val), C["green"] if success_count > 0 else C["red"])

        g._refresh_cheat_tree()
        self.destroy()

    def _center(self):
        self.update_idletasks()
        r = self._gui.root
        x = r.winfo_x() + (r.winfo_width()  - self.winfo_width())  // 2
        y = r.winfo_y() + (r.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")



# ─────────────────────────────────────────────────────────────────────────────
# MANUEL ADRES EKLEME DİYALOĞU
# ─────────────────────────────────────────────────────────────────────────────
class ManualAddDialog(tk.Toplevel):
    def __init__(self, gui):
        super().__init__(gui.root)
        self._gui = gui

        self.title(f"{gui.t('manual_dialog_title')} — Spexron Engine")
        self.geometry("450x380")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self.transient(gui.root)
        self.grab_set()
        self._build()
        self._center()

    def _build(self):
        g = self._gui

        # Header
        hdr = tk.Frame(self, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        tk.Frame(hdr, bg=C["accent"], width=3).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(hdr, text=f"  +  {g.t('manual_dialog_title')}",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 11, "bold"), pady=12
                 ).pack(side=tk.LEFT)
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)
        body.columnconfigure(1, weight=1)

        # Address Input
        tk.Label(body, text=g.t("manual_dialog_prompt_addr"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=8)
        self._ent_addr = tk.Entry(body, bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"],
                                  font=("Consolas", 11), relief=tk.FLAT, highlightthickness=1,
                                  highlightbackground=C["border"], highlightcolor=C["accent"])
        self._ent_addr.grid(row=0, column=1, sticky=tk.EW, padx=(12, 0), pady=8, ipady=4)
        self._ent_addr.focus_set()

        # Description Input
        tk.Label(body, text=g.t("manual_dialog_prompt_desc"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=8)
        self._ent_desc = tk.Entry(body, bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"],
                                  font=("Segoe UI", 10), relief=tk.FLAT, highlightthickness=1,
                                  highlightbackground=C["border"], highlightcolor=C["accent"])
        self._ent_desc.grid(row=1, column=1, sticky=tk.EW, padx=(12, 0), pady=8, ipady=4)
        self._ent_desc.insert(0, g.t("desc_default"))

        # Value Type Dropdown
        tk.Label(body, text=g.t("manual_dialog_prompt_type"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky=tk.W, pady=8)
        
        # Translate dropdown options
        vt_opts = [g.t(k) for k in ("val_1byte", "val_2bytes", "val_4bytes", "val_8bytes", "val_float", "val_double")]
        self._cmb_type = ModernCombo(body, values=vt_opts, state="readonly", style="TCombobox")
        self._cmb_type.grid(row=2, column=1, sticky=tk.EW, padx=(12, 0), pady=8)
        self._cmb_type.set(g.t("val_4bytes"))

        # Value Input
        tk.Label(body, text=g.t("manual_dialog_prompt_val"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky=tk.W, pady=8)
        self._ent_val = tk.Entry(body, bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"],
                                 font=("Consolas", 11), relief=tk.FLAT, highlightthickness=1,
                                 highlightbackground=C["border"], highlightcolor=C["accent"])
        self._ent_val.grid(row=3, column=1, sticky=tk.EW, padx=(12, 0), pady=8, ipady=4)
        self._ent_val.insert(0, "0")

        # Buttons
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)
        btn_row = tk.Frame(self, bg=C["surface"])
        btn_row.pack(fill=tk.X, padx=18, pady=12)

        ModernButton(btn_row, text=g.t("picker_btn_cancel"),
                     style="default", command=self.destroy
                     ).pack(side=tk.LEFT)

        ModernButton(btn_row, text=f"✔  {g.t('btn_add_confirm')}",
                     style="primary", command=self._apply
                     ).pack(side=tk.RIGHT)

        self.bind("<Return>",  lambda _: self._apply())
        self.bind("<Escape>",  lambda _: self.destroy())

    def _apply(self):
        g = self._gui
        addr_str = self._ent_addr.get().strip()
        desc = self._ent_desc.get().strip() or g.t("desc_default")
        val = self._ent_val.get().strip() or "0"
        
        # Verify hex address
        try:
            if addr_str.lower().startswith("0x"):
                addr = int(addr_str, 16)
            else:
                addr = int(addr_str, 16)
            key = f"0x{addr:016X}"
        except Exception:
            messagebox.showerror(g.t("manual_dialog_title"), g.t("manual_dialog_err_invalid"), parent=self)
            return

        # Resolve type backend string from dynamic translation
        selected_type = self._cmb_type.get()
        vt = _build_val_type_map(LOCALIZATION, g.current_lang).get(selected_type, "4 Bytes")

        # Save record
        g.saved_cheats[key] = {
            "description": desc,
            "type":  vt,
            "value": val,
            "locked": False,
        }
        g._refresh_cheat_tree()
        g.log(g.t("manual_dialog_success", key), C["gold"])
        self.destroy()

    def _center(self):
        self.update_idletasks()
        r = self._gui.root
        x = r.winfo_x() + (r.winfo_width()  - self.winfo_width())  // 2
        y = r.winfo_y() + (r.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


# ─────────────────────────────────────────────────────────────────────────────
# GELİŞMİŞ AYARLAR DİYALOĞU
# ─────────────────────────────────────────────────────────────────────────────
class SettingsDialog(tk.Toplevel):
    def __init__(self, gui):
        super().__init__(gui.root)
        self._gui = gui

        self.title(f"{gui.t('settings_dialog_title')} — Spexron Engine")
        self.geometry("740x580")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self.transient(gui.root)
        self.grab_set()
        self._build()
        self._center()

    def _build(self):
        g = self._gui

        # Header
        hdr = tk.Frame(self, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        tk.Frame(hdr, bg=C["accent"], width=3).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(hdr, text=f"  ⚙  {g.t('settings_dialog_title')}",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 11, "bold"), pady=12
                 ).pack(side=tk.LEFT)
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)

        # Tabbed Sidebar & Content Framework
        container = tk.Frame(self, bg=C["bg"])
        container.pack(fill=tk.BOTH, expand=True)

        self._sidebar = tk.Frame(container, bg=C["surface2"], width=180)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self._sidebar.pack_propagate(False)

        self._divider = tk.Frame(container, bg=C["border"], width=1)
        self._divider.pack(side=tk.LEFT, fill=tk.Y)

        self._content_wrap = tk.Frame(container, bg=C["bg"])
        self._content_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Content frames for tabs
        self._tab_general = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_scan = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_hotkeys = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_debugger = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_speedhack = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_appearance = tk.Frame(self._content_wrap, bg=C["bg"])
        self._tab_about = tk.Frame(self._content_wrap, bg=C["bg"])

        # ── Sidebar Navigation Custom Tabs ──
        self._tabs = {}
        for tab_name, key in [
            ("general", "settings_tab_general"),
            ("scan", "settings_tab_scan"),
            ("hotkeys", "settings_tab_hotkeys"),
            ("debugger", "settings_tab_debugger"),
            ("speedhack", "settings_tab_speedhack"),
            ("appearance", "settings_tab_appearance"),
            ("about", "settings_tab_about")
        ]:
            label = g.t(key)
            tab = SidebarTab(self._sidebar, text=label, command=lambda tn=tab_name: self._switch_tab(tn))
            tab.pack(fill=tk.X, padx=6, pady=3)
            self._tabs[tab_name] = tab

        # ── Genel (General) Tab Content ──
        card_gen_attach = SectionCard(self._tab_general, title=g.t("settings_lbl_auto_attach"), accent=C["accent"])
        card_gen_attach.pack(fill=tk.X, pady=(0, 10))
        
        self._var_auto_attach = tk.BooleanVar(value=g.auto_attach)
        self._chk_auto_attach = tk.Checkbutton(
            card_gen_attach.body, text=g.t("settings_lbl_auto_attach"),
            variable=self._var_auto_attach, bg=C["surface"], fg=C["text"],
            selectcolor=C["surface2"], activebackground=C["surface"],
            activeforeground=C["accent"], font=("Segoe UI", 9, "bold")
        )
        self._chk_auto_attach.pack(anchor=tk.W, padx=12, pady=6)
        
        lbl_proc = tk.Label(card_gen_attach.body, text=g.t("settings_lbl_auto_attach_proc"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9))
        lbl_proc.pack(anchor=tk.W, padx=12, pady=(0, 2))
        self._ent_auto_attach_proc = ModernEntry(card_gen_attach.body)
        self._ent_auto_attach_proc.pack(fill=tk.X, padx=12, pady=(0, 12))
        self._ent_auto_attach_proc.insert(0, g.auto_attach_process)

        card_gen_misc = SectionCard(self._tab_general, title=g.t("settings_tab_general"), accent=C["accent"])
        card_gen_misc.pack(fill=tk.X, pady=10)

        self._var_show_hex = tk.BooleanVar(value=g.show_hex)
        self._chk_show_hex = tk.Checkbutton(
            card_gen_misc.body, text=g.t("settings_lbl_show_hex"),
            variable=self._var_show_hex, bg=C["surface"], fg=C["text"],
            selectcolor=C["surface2"], activebackground=C["surface"],
            activeforeground=C["accent"], font=("Segoe UI", 9, "bold")
        )
        self._chk_show_hex.pack(anchor=tk.W, padx=12, pady=6)

        self._var_show_status_bar = tk.BooleanVar(value=g.show_status_bar)
        self._chk_show_status_bar = tk.Checkbutton(
            card_gen_misc.body, text=g.t("settings_lbl_show_status_bar"),
            variable=self._var_show_status_bar, bg=C["surface"], fg=C["text"],
            selectcolor=C["surface2"], activebackground=C["surface"],
            activeforeground=C["accent"], font=("Segoe UI", 9, "bold")
        )
        self._chk_show_status_bar.pack(anchor=tk.W, padx=12, pady=6)

        self._var_confirm_close = tk.BooleanVar(value=g.confirm_close)
        self._chk_confirm_close = tk.Checkbutton(
            card_gen_misc.body, text=g.t("settings_lbl_confirm_close"),
            variable=self._var_confirm_close, bg=C["surface"], fg=C["text"],
            selectcolor=C["surface2"], activebackground=C["surface"],
            activeforeground=C["accent"], font=("Segoe UI", 9, "bold")
        )
        self._chk_confirm_close.pack(anchor=tk.W, padx=12, pady=6)

        card_gen_rates = SectionCard(self._tab_general, title=g.t("settings_lbl_update_rate"), accent=C["accent"])
        card_gen_rates.pack(fill=tk.X, pady=10)
        
        lbl_rate = tk.Label(card_gen_rates.body, text=g.t("settings_lbl_update_rate"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold"))
        lbl_rate.pack(side=tk.LEFT, padx=12, pady=12)
        self._cmb_update_rate = ModernCombo(card_gen_rates.body, values=["100 ms", "200 ms", "500 ms", "1000 ms", "2000 ms"], state="readonly")
        self._cmb_update_rate.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=12, pady=12)
        self._cmb_update_rate.set(f"{int(g.update_interval * 1000)} ms")

        # ── Tarama (Scan) Tab Content ──
        card_scan_range = SectionCard(self._tab_scan, title=g.t("settings_lbl_start_addr") + " / " + g.t("settings_lbl_end_addr"), accent=C["accent"])
        card_scan_range.pack(fill=tk.X, pady=(0, 10))

        grid_f = tk.Frame(card_scan_range.body, bg=C["surface"])
        grid_f.pack(fill=tk.X, padx=12, pady=8)
        grid_f.columnconfigure(1, weight=1)

        tk.Label(grid_f, text=g.t("settings_lbl_start_addr"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=4)
        self._ent_start_addr = ModernEntry(grid_f)
        self._ent_start_addr.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=4)
        self._ent_start_addr.insert(0, g.scan_start_addr)

        tk.Label(grid_f, text=g.t("settings_lbl_end_addr"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=4)
        self._ent_end_addr = ModernEntry(grid_f)
        self._ent_end_addr.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=4)
        self._ent_end_addr.insert(0, g.scan_end_addr)

        card_scan_types = SectionCard(self._tab_scan, title=g.t("settings_lbl_mem_types"), accent=C["accent"])
        card_scan_types.pack(fill=tk.X, pady=10)

        checks_f = tk.Frame(card_scan_types.body, bg=C["surface"])
        checks_f.pack(fill=tk.X, padx=12, pady=6)
        
        self._var_mem_private = tk.BooleanVar(value=g.scan_mem_private)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_mem_private"), variable=self._var_mem_private, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=2)
        
        self._var_mem_image = tk.BooleanVar(value=g.scan_mem_image)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_mem_image"), variable=self._var_mem_image, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=2)
        
        self._var_mem_mapped = tk.BooleanVar(value=g.scan_mem_mapped)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_mem_mapped"), variable=self._var_mem_mapped, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=2)

        self._var_writable_only = tk.BooleanVar(value=g.scan_writable_only)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_writable"), variable=self._var_writable_only, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=4)

        self._var_mem_executable = tk.BooleanVar(value=g.scan_mem_executable)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_protect_executable"), variable=self._var_mem_executable, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=2)

        self._var_mem_copy_on_write = tk.BooleanVar(value=g.scan_mem_copy_on_write)
        tk.Checkbutton(checks_f, text=g.t("settings_lbl_protect_copy_on_write"), variable=self._var_mem_copy_on_write, bg=C["surface"], fg=C["text"], selectcolor=C["surface2"], activebackground=C["surface"], activeforeground=C["accent"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=2)

        card_scan_misc = SectionCard(self._tab_scan, title=g.t("settings_lbl_alignment"), accent=C["accent"])
        card_scan_misc.pack(fill=tk.X, pady=10)

        misc_f = tk.Frame(card_scan_misc.body, bg=C["surface"])
        misc_f.pack(fill=tk.X, padx=12, pady=6)
        misc_f.columnconfigure(1, weight=1)

        tk.Label(misc_f, text=g.t("settings_lbl_alignment"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=4)
        self._cmb_align = ModernCombo(misc_f, values=["1", "2", "4", "8"], state="readonly")
        self._cmb_align.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=4)
        self._cmb_align.set(str(g.align_bytes))

        tk.Label(misc_f, text=g.t("settings_lbl_threads"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=4)
        self._cmb_threads = ModernCombo(misc_f, values=["1", "2", "4", "8", "16"], state="readonly")
        self._cmb_threads.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=4)
        self._cmb_threads.set(str(g.scan_threads))

        tk.Label(misc_f, text=g.t("settings_lbl_limit"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky=tk.W, pady=4)
        self._cmb_limit = ModernCombo(misc_f, values=["100", "250", "500", "1000", "5000"], state="readonly")
        self._cmb_limit.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=4)
        self._cmb_limit.set(str(g.max_display_results))

        # ── Kısayollar (Hotkeys) Tab Content ──
        card_hk = SectionCard(self._tab_hotkeys, title=g.t("settings_tab_hotkeys"), accent=C["accent"])
        card_hk.pack(fill=tk.BOTH, expand=True)

        hk_f = tk.Frame(card_hk.body, bg=C["surface"])
        hk_f.pack(fill=tk.X, padx=12, pady=8)
        hk_f.columnconfigure(1, weight=1)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_select_proc"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=6)
        self._ent_hk_select_proc = ModernEntry(hk_f)
        self._ent_hk_select_proc.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_select_proc.insert(0, g.hotkey_select_proc)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_pause_proc"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=6)
        self._ent_hk_pause_proc = ModernEntry(hk_f)
        self._ent_hk_pause_proc.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_pause_proc.insert(0, g.hotkey_pause_proc)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_freeze_addr"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky=tk.W, pady=6)
        self._ent_hk_freeze_addr = ModernEntry(hk_f)
        self._ent_hk_freeze_addr.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_freeze_addr.insert(0, g.hotkey_freeze_addr)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_speedhack"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky=tk.W, pady=6)
        self._ent_hk_speedhack = ModernEntry(hk_f)
        self._ent_hk_speedhack.grid(row=3, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_speedhack.insert(0, g.hotkey_speedhack)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_next_scan"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky=tk.W, pady=6)
        self._ent_hk_next_scan = ModernEntry(hk_f)
        self._ent_hk_next_scan.grid(row=4, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_next_scan.insert(0, g.hotkey_next_scan)

        tk.Label(hk_f, text=g.t("settings_lbl_hk_reset_scan"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky=tk.W, pady=6)
        self._ent_hk_reset_scan = ModernEntry(hk_f)
        self._ent_hk_reset_scan.grid(row=5, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._ent_hk_reset_scan.insert(0, g.hotkey_reset_scan)

        # ── Hata Ayıklayıcı (Debugger) Tab Content ──
        card_dbg = SectionCard(self._tab_debugger, title=g.t("settings_tab_debugger"), accent=C["accent"])
        card_dbg.pack(fill=tk.X, pady=(0, 10))

        dbg_f = tk.Frame(card_dbg.body, bg=C["surface"])
        dbg_f.pack(fill=tk.X, padx=12, pady=8)
        dbg_f.columnconfigure(1, weight=1)

        tk.Label(dbg_f, text=g.t("settings_lbl_dbg_type"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=6)
        self._cmb_dbg_type = ModernCombo(dbg_f, values=["Windows Debugger", "VEH Debugger", "DBVM Debugger"], state="readonly")
        self._cmb_dbg_type.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._cmb_dbg_type.set(g.debugger_type)

        tk.Label(dbg_f, text=g.t("settings_lbl_bp_type"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=6)
        self._cmb_bp_type = ModernCombo(dbg_f, values=["Hardware Breakpoint", "Software Breakpoint"], state="readonly")
        self._cmb_bp_type.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._cmb_bp_type.set(g.breakpoint_type)

        card_dbg_hw = SectionCard(self._tab_debugger, title=g.t("settings_lbl_dbg_hardware_type"), accent=C["accent"])
        card_dbg_hw.pack(fill=tk.X, pady=10)

        hw_f = tk.Frame(card_dbg_hw.body, bg=C["surface"])
        hw_f.pack(fill=tk.X, padx=12, pady=8)
        hw_f.columnconfigure(1, weight=1)

        tk.Label(hw_f, text=g.t("settings_lbl_dbg_hardware_type"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=6)
        self._cmb_hw_type = ModernCombo(hw_f, values=["Write", "Read/Write", "Execute"], state="readonly")
        self._cmb_hw_type.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
        self._cmb_hw_type.set(g.hardware_bp_type)

        # ── Speedhack Tab Content ──
        card_sh = SectionCard(self._tab_speedhack, title=g.t("settings_tab_speedhack"), accent=C["accent"])
        card_sh.pack(fill=tk.BOTH, expand=True)

        sh_f = tk.Frame(card_sh.body, bg=C["surface"])
        sh_f.pack(fill=tk.X, padx=12, pady=8)
        sh_f.columnconfigure(1, weight=1)

        self._var_sh_enable = tk.BooleanVar(value=g.speedhack_enabled)
        self._chk_sh_enable = tk.Checkbutton(
            sh_f, text=g.t("settings_lbl_sh_enable"),
            variable=self._var_sh_enable, bg=C["surface"], fg=C["text"],
            selectcolor=C["surface2"], activebackground=C["surface"],
            activeforeground=C["accent"], font=("Segoe UI", 9, "bold")
        )
        self._chk_sh_enable.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=8)

        tk.Label(sh_f, text=g.t("settings_lbl_sh_speed"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=8)
        self._ent_sh_speed = ModernEntry(sh_f)
        self._ent_sh_speed.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=8)
        self._ent_sh_speed.insert(0, g.speedhack_speed)

        # ── Görünüm (Appearance) Tab Content ──
        card_app = SectionCard(self._tab_appearance, title=g.t("settings_tab_appearance"), accent=C["accent"])
        card_app.pack(fill=tk.BOTH, expand=True)

        app_f = tk.Frame(card_app.body, bg=C["surface"])
        app_f.pack(fill=tk.X, padx=12, pady=8)
        app_f.columnconfigure(1, weight=1)

        tk.Label(app_f, text=g.t("settings_lbl_freeze_rate"), bg=C["surface"], fg=C["text_muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        self._cmb_freeze = ModernCombo(app_f, values=["50 ms", "100 ms", "200 ms", "500 ms"], state="readonly")
        self._cmb_freeze.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=10)
        self._cmb_freeze.set(f"{int(g.freeze_interval * 1000)} ms")

        # ── Hakkımda (About Me) Tab Content with Logo ──
        logo_lbl = tk.Label(
            self._tab_about, text="SPEXRON ENGINE",
            bg=C["bg"], fg="#FFD700",
            font=("Segoe UI", 20, "bold")
        )
        logo_lbl.pack(pady=(20, 6))
        logo_lbl.theme_bg = "bg"


        
        about_credit = tk.Label(
            self._tab_about, 
            text="SPEXRON tarafından kodlanmıştır.\nCoded by SPEXRON.\n\nTüm hakları saklıdır. © 2026\nAll rights reserved.",
            bg=C["bg"], fg=C["text"],
            font=("Segoe UI", 9, "bold"),
            justify=tk.CENTER
        )
        about_credit.pack(pady=6)

        # Buttons Row (Always visible at the bottom)
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)
        btn_row = tk.Frame(self, bg=C["surface2"])
        btn_row.pack(fill=tk.X, padx=18, pady=12)

        ModernButton(btn_row, text=g.t("picker_btn_cancel"),
                     style="default", command=self.destroy
                     ).pack(side=tk.LEFT)

        ModernButton(btn_row, text=f"✔  {g.t('settings_btn_save')}",
                     style="primary", command=self._apply
                     ).pack(side=tk.RIGHT)

        # Switch to default general tab
        self._switch_tab("general")

        self.bind("<Return>",  lambda _: self._apply())
        self.bind("<Escape>",  lambda _: self.destroy())

    def _switch_tab(self, name):
        self._tab_general.pack_forget()
        self._tab_scan.pack_forget()
        self._tab_hotkeys.pack_forget()
        self._tab_debugger.pack_forget()
        self._tab_speedhack.pack_forget()
        self._tab_appearance.pack_forget()
        self._tab_about.pack_forget()

        for tab_name, tab in self._tabs.items():
            if tab_name == name:
                tab.update_state(True)
            else:
                tab.update_state(False)

        if name == "general":
            self._tab_general.pack(fill=tk.BOTH, expand=True)
        elif name == "scan":
            self._tab_scan.pack(fill=tk.BOTH, expand=True)
        elif name == "hotkeys":
            self._tab_hotkeys.pack(fill=tk.BOTH, expand=True)
        elif name == "debugger":
            self._tab_debugger.pack(fill=tk.BOTH, expand=True)
        elif name == "speedhack":
            self._tab_speedhack.pack(fill=tk.BOTH, expand=True)
        elif name == "appearance":
            self._tab_appearance.pack(fill=tk.BOTH, expand=True)
        elif name == "about":
            self._tab_about.pack(fill=tk.BOTH, expand=True)

    def _apply(self):
        g = self._gui
        try:
            # Genel Tab
            g.auto_attach = self._var_auto_attach.get()
            g.auto_attach_process = self._ent_auto_attach_proc.get().strip()
            g.show_hex = self._var_show_hex.get()
            g.confirm_close = self._var_confirm_close.get()
            
            wants_status_bar = self._var_show_status_bar.get()
            if wants_status_bar != g.show_status_bar:
                g.show_status_bar = wants_status_bar
                if hasattr(g, "statusbar"):
                    if wants_status_bar:
                        g.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
                    else:
                        g.statusbar.pack_forget()
            
            update_rate_str = self._cmb_update_rate.get().split()[0]
            g.update_interval = int(update_rate_str) / 1000.0

            # Tarama Tab
            g.scan_start_addr = self._ent_start_addr.get().strip()
            g.scan_end_addr = self._ent_end_addr.get().strip()
            
            g.scan_mem_private = self._var_mem_private.get()
            g.scan_mem_image = self._var_mem_image.get()
            g.scan_mem_mapped = self._var_mem_mapped.get()
            g.scan_writable_only = self._var_writable_only.get()
            g.scan_mem_executable = self._var_mem_executable.get()
            g.scan_mem_copy_on_write = self._var_mem_copy_on_write.get()
            
            g.align_bytes = int(self._cmb_align.get())
            g.scan_threads = int(self._cmb_threads.get())
            g.max_display_results = int(self._cmb_limit.get())

            # Kısayollar Tab
            g.hotkey_select_proc = self._ent_hk_select_proc.get().strip()
            g.hotkey_pause_proc = self._ent_hk_pause_proc.get().strip()
            g.hotkey_freeze_addr = self._ent_hk_freeze_addr.get().strip()
            g.hotkey_speedhack = self._ent_hk_speedhack.get().strip()
            g.hotkey_next_scan = self._ent_hk_next_scan.get().strip()
            g.hotkey_reset_scan = self._ent_hk_reset_scan.get().strip()

            # Hata Ayıklayıcı Tab
            g.debugger_type = self._cmb_dbg_type.get()
            g.breakpoint_type = self._cmb_bp_type.get()
            g.hardware_bp_type = self._cmb_hw_type.get()

            # Speedhack Tab
            g.speedhack_enabled = self._var_sh_enable.get()
            g.speedhack_speed = self._ent_sh_speed.get().strip()

            # Görünüm Tab
            freeze_rate_str = self._cmb_freeze.get().split()[0]
            g.freeze_interval = int(freeze_rate_str) / 1000.0

            # Apply scanner limits immediately
            g._apply_settings_to_scanner()
            # Apply hotkey changes immediately
            g._bind_hotkeys()
        except Exception:
            pass
        g.log(g.t("settings_success"), C["green"])
        self.destroy()

    def _center(self):
        self.update_idletasks()
        r = self._gui.root
        x = r.winfo_x() + (r.winfo_width()  - self.winfo_width())  // 2
        y = r.winfo_y() + (r.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")


class ModernContextMenu(tk.Toplevel):
    def __init__(self, gui, parent=None):
        super().__init__(parent or gui.root)
        self.gui = gui
        self.owner = None
        self.overrideredirect(True)
        self.withdraw() # Start hidden until tk_popup is called
        self.configure(bg=C["border"])
        self.attributes("-topmost", True)
        
        # 1-pixel border inner container
        self.inner = tk.Frame(self, bg=C["surface"], padx=2, pady=2)
        self.inner.pack(fill=tk.BOTH, expand=True)
        
        # Destroy previous active menu if any
        if hasattr(gui, "active_menu") and gui.active_menu:
            try:
                gui.active_menu.destroy()
            except Exception:
                pass
        gui.active_menu = self
        
        # Self-destruct when clicking away or losing focus
        self.bind("<FocusOut>", lambda _: self.destroy())
        
        # Bind global left-click to destroy this menu if clicked outside (delayed to prevent immediate self-destruction)
        self._click_bind = None
        self._click_bind_timer = self.after(100, self._setup_global_click)

    def _setup_global_click(self):
        self._click_bind_timer = None
        try:
            self._click_bind = self.gui.root.bind_all("<Button-1>", self._on_global_click, add="+")
        except Exception:
            pass

    def _on_global_click(self, event):
        w = event.widget
        curr = w
        while curr:
            if curr == self:
                return
            try:
                curr = curr.master
            except AttributeError:
                break
        self.destroy()

    def add_command(self, label, command=None, icon="", is_danger=False):
        row = tk.Frame(self.inner, bg=C["surface"], cursor="hand2")
        row.pack(fill=tk.X, pady=1)
        
        fg_color = C["red"] if is_danger else C["text2"]
        
        # Icon Label
        lbl_icon = tk.Label(row, text=f" {icon}  " if icon else "    ", 
                            bg=C["surface"], fg=fg_color,
                            font=("Segoe UI", 9), anchor=tk.W)
        lbl_icon.pack(side=tk.LEFT, padx=(6, 0), pady=4)
        
        # Text Label
        lbl_text = tk.Label(row, text=label, 
                            bg=C["surface"], fg=fg_color,
                            font=("Segoe UI", 9, "bold"), anchor=tk.W)
        lbl_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 16), pady=4)
        
        # Bind events
        def on_enter(_):
            row.config(bg=C["surface3"])
            lbl_icon.config(bg=C["surface3"])
            lbl_text.config(bg=C["surface3"])
            if not is_danger:
                lbl_icon.config(fg=C["accent"])
                lbl_text.config(fg=C["accent"])
                
        def on_leave(_):
            row.config(bg=C["surface"])
            lbl_icon.config(bg=C["surface"])
            lbl_text.config(bg=C["surface"])
            lbl_icon.config(fg=fg_color)
            lbl_text.config(fg=fg_color)
            
        def on_click(_):
            self.destroy()
            if command:
                command()
                
        for widget in (row, lbl_icon, lbl_text):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

    def add_separator(self):
        sep = tk.Frame(self.inner, bg=C["border"], height=1)
        sep.pack(fill=tk.X, padx=4, pady=3)

    def tk_popup(self, x, y):
        # Update geometry and lift window to top
        self.deiconify()
        self.geometry(f"+{x}+{y}")
        self.focus_set()

    def destroy(self):
        # Cancel the pending timer if any
        if hasattr(self, "_click_bind_timer") and self._click_bind_timer:
            try:
                self.after_cancel(self._click_bind_timer)
            except Exception:
                pass
            self._click_bind_timer = None
        # Unbind global click when menu is destroyed
        if hasattr(self, "_click_bind") and self._click_bind:
            try:
                self.gui.root.unbind_all("<Button-1>", self._click_bind)
            except Exception:
                pass
            self._click_bind = None
        if getattr(self.gui, "active_menu", None) == self:
            self.gui.active_menu = None
        super().destroy()


class CheatContextMenu(ModernContextMenu):
    def __init__(self, gui, addr, info):
        super().__init__(gui)
        t = gui.t

        self.add_command(t("ctx_change_value"), icon="✎",
                         command=lambda: gui._show_value_editor(addr, info))
        self.add_command(t("ctx_set_value"), icon="⚡",
                         command=lambda: gui._ctx_set_value(addr, info))
        self.add_command("Gösterge/Offset Tara (Pointer Scan)", icon="🔍",
                         command=lambda: gui._open_pointer_scanner(addr))
        self.add_separator()
        if info["locked"]:
            self.add_command(t("ctx_unfreeze"), icon="🔓",
                             command=lambda: gui._ctx_toggle_freeze(addr, False))
        else:
            self.add_command(t("ctx_freeze"), icon="🔒",
                             command=lambda: gui._ctx_toggle_freeze(addr, True))
        self.add_separator()
        self.add_command(t("ctx_edit_desc"), icon="📝",
                         command=lambda: gui._ctx_edit_desc(addr, info))
        self.add_command(t("ctx_edit_type"), icon="⚙",
                         command=lambda: gui._ctx_edit_type(addr, info))
        self.add_separator()
        self.add_command(t("ctx_remove"), icon="✕", is_danger=True,
                         command=lambda: gui._ctx_remove(addr))


class FoundContextMenu(ModernContextMenu):
    def __init__(self, gui, addr):
        super().__init__(gui)
        self.add_command("Tabloya Ekle (Add to Table)", icon="➕",
                         command=gui._add_selected_to_cheat_table)
        self.add_command("Gösterge/Offset Tara (Pointer Scan)", icon="🔍",
                         command=lambda: gui._open_pointer_scanner(addr))


# ─────────────────────────────────────────────────────────────────────────────
# ANA PENCERE
# ─────────────────────────────────────────────────────────────────────────────
class SpexronEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spexron Engine | Memory Scanner")
        self.root.geometry("1100x820")
        self.root.minsize(900, 660)
        self.root.resizable(True, True)
        self.root.configure(bg=C["bg"])

        self.current_theme        = "dark"
        self.scanner              = None
        self.target_pid           = None
        self.current_process_name = None
        self.saved_cheats         = {}
        self.lock_thread_active   = True
        self.current_lang         = "tr"

        # Advanced Settings Options
        self.align_bytes          = 4
        self.scan_threads         = 4
        self.max_display_results  = 250
        self.freeze_interval      = 0.1

        # Gelişmiş Cheat Engine Tarzı Ayarlar
        self.scan_start_addr      = "0x00000000"
        self.scan_end_addr        = "0x7FFFFFFFFFFF"
        self.scan_mem_private     = True
        self.scan_mem_image       = True
        self.scan_mem_mapped      = False
        self.scan_writable_only   = True
        self.scan_mem_executable  = False
        self.scan_mem_copy_on_write = False

        self.auto_attach          = False
        self.auto_attach_process  = "tutorial-x86_64.exe"
        self.show_hex             = False
        self.show_status_bar      = True
        self.update_interval      = 0.5
        self.confirm_close        = True

        self.hotkey_select_proc   = "Ctrl+Alt+P"
        self.hotkey_pause_proc    = "Pause"
        self.hotkey_freeze_addr   = "Space"
        self.hotkey_speedhack     = "F4"
        self.hotkey_next_scan     = "F3"
        self.hotkey_reset_scan    = "F2"

        self.debugger_type        = "Windows Debugger"
        self.breakpoint_type      = "Hardware Breakpoint"
        self.hardware_bp_type     = "Write"

        self.speedhack_enabled    = False
        self.speedhack_speed      = "1.0"

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._ttk_styles()         # Önce style tanımla
        self._build()               # Sonra widget'ları oluştur
        self._lang_update()
        self._setup_global_bindings()
        self._bind_hotkeys()

        threading.Thread(target=self._freezer_loop, daemon=True).start()
        self.root.after(500, self._live_update_tick)
        self.lbl_status.config(text=f"  ○  {self.t('status_disconnected')}",
                               fg=C["text_muted"])
        self.log(self.t("log_awaiting"))

    def _on_close(self):
        if self.confirm_close:
            title = self.t("settings_confirm_close_title")
            msg = self.t("settings_confirm_close_msg")
            if not messagebox.askyesno(title, msg, parent=self.root):
                return
        self.root.destroy()

    def t(self, key, *args):
        text = LOCALIZATION[self.current_lang].get(key, key)
        return text.format(*args) if args else text

    def _setup_global_bindings(self):
        def select_all(event):
            event.widget.select_range(0, tk.END)
            event.widget.icursor(tk.END)
            return "break"

        def delete_word(event):
            entry = event.widget
            contents = entry.get()
            insert_idx = entry.index(tk.INSERT)
            if insert_idx == 0:
                return "break"
            text_to_search = contents[:insert_idx].rstrip()
            if not text_to_search:
                entry.delete(0, insert_idx)
                return "break"
            space_idx = text_to_search.rfind(' ')
            if space_idx == -1:
                entry.delete(0, insert_idx)
            else:
                entry.delete(space_idx + 1, insert_idx)
            return "break"

        def select_all_tree(event):
            tree = event.widget
            tree.selection_set(tree.get_children())
            return "break"

        def copy_tree_selection(event):
            tree = event.widget
            selected = tree.selection()
            if not selected:
                return "break"
            lines = []
            for item in selected:
                vals = tree.item(item, "values")
                lines.append("\t".join(str(v) for v in vals))
            text = "\n".join(lines)
            tree.clipboard_clear()
            tree.clipboard_append(text)
            return "break"

        self.root.bind_class("Entry", "<Control-a>", select_all)
        self.root.bind_class("Entry", "<Control-A>", select_all)
        self.root.bind_class("Entry", "<Control-BackSpace>", delete_word)
        self.root.bind_class("Treeview", "<Control-a>", select_all_tree)
        self.root.bind_class("Treeview", "<Control-A>", select_all_tree)
        self.root.bind_class("Treeview", "<Control-c>", copy_tree_selection)
        self.root.bind_class("Treeview", "<Control-C>", copy_tree_selection)

    def _translate_val_type(self, val_type):
        m = {
            "1 Byte":   "val_1byte",
            "2 Bytes":  "val_2bytes",
            "4 Bytes":  "val_4bytes",
            "8 Bytes":  "val_8bytes",
            "Float":    "val_float",
            "Double":   "val_double",
        }
        key = m.get(val_type)
        return self.t(key) if key else val_type

    # ═══════════════════════════════════════════════════════════════════════
    # TTK STYLES
    # ═══════════════════════════════════════════════════════════════════════
    def _ttk_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        # Bug fix for Python 3.8+ Treeview tag colors (ignores tag configure colors on native themes/clam)
        def fixed_map(option):
            return [elm for elm in s.map("Treeview", query_opt=option)
                    if elm[:2] != ("!disabled", "!selected")]
        s.map("Treeview", 
              foreground=fixed_map("foreground"), 
              background=fixed_map("background"))

        # Progressbar — ultra-thin Zinc indicator
        s.configure("TProgressbar",
                    thickness=4,
                    troughcolor=C["progress_bg"],
                    background=C["progress_fill"],
                    borderwidth=0)

        # Combobox — flat modern dropdown styling
        s.configure("TCombobox",
                    background=C["surface2"],
                    foreground=C["text"],
                    fieldbackground=C["surface2"],
                    selectbackground=C["accent_dim"],
                    selectforeground=C["accent"],
                    arrowcolor=C["text_muted"],
                    insertcolor=C["text"],
                    borderwidth=0,
                    relief="flat",
                    padding=6)
        s.map("TCombobox",
              fieldbackground=[("readonly", C["surface2"])],
              foreground=[("readonly", C["text"])],
              background=[("readonly", C["surface2"])],
              borderwidth=[("readonly", 0)],
              relief=[("readonly", "flat")])

        # Modern Horizontal Scale Style (zinc trough + blue thumb)
        s.configure("Modern.Horizontal.TScale",
                    troughcolor=C["border"],
                    background=C["accent"],
                    slidercolor=C["accent"],
                    lightcolor=C["border"],
                    darkcolor=C["border"],
                    borderwidth=0,
                    sliderthickness=12)
        s.map("Modern.Horizontal.TScale",
              background=[("active", C["btn_primary_h"])])

        # Modern Scrollbar Layout (No up/down arrow buttons, fully flat)
        s.layout("Modern.Vertical.TScrollbar", [
            ("Vertical.Scrollbar.trough", {
                "children": [
                    ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"})
                ],
                "sticky": "ns"
            })
        ])

        # Scrollbar — minimal flat indicators
        s.configure("Modern.Vertical.TScrollbar",
                    background=C.get("sb_thumb", C["surface2"]),
                    troughcolor=C.get("sb_trough", C["bg"]),
                    bordercolor=C.get("sb_trough", C["bg"]),
                    lightcolor=C.get("sb_thumb", C["surface2"]),
                    darkcolor=C.get("sb_thumb", C["surface2"]),
                    gripcount=0,
                    width=10,
                    borderwidth=0, relief="flat")
        s.map("Modern.Vertical.TScrollbar",
              background=[("active", C.get("sb_thumb_hover", C["surface3"]))],
              lightcolor=[("active", C.get("sb_thumb_hover", C["surface3"]))],
              darkcolor=[("active", C.get("sb_thumb_hover", C["surface3"]))])

        # Universal Treeview Styling — spacious premium solid dark grid (#1E1E1E)
        s.configure("Treeview",
                    background=C["surface"],
                    foreground=C["text2"],
                    fieldbackground=C["surface"],
                    rowheight=26,
                    borderwidth=1,
                    relief="flat",
                    bordercolor=C["border"],
                    lightcolor=C["border"],
                    darkcolor=C["border"],
                    font=("Segoe UI", 9))
        
        # WIPE OUT any native Vista state-specific maps by replacing them entirely!
        s.map("Treeview",
              background=[("selected", C["sel_found"])],
              foreground=[("selected", C["sel_found_fg"])])

        s.configure("Treeview.Heading",
                    background=C["surface2"],
                    foreground=C["text_muted"],
                    font=("Segoe UI", 8, "bold"),
                    relief="flat",
                    borderwidth=1,
                    bordercolor=C["border"],
                    lightcolor=C["border"],
                    darkcolor=C["border"],
                    padding=6)
        s.map("Treeview.Heading",
              background=[("active", C["surface3"])],
              foreground=[("active", C["text"])])

    def _toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self._apply_theme()
        self._lang_update()

    def _apply_theme(self):
        theme_palette = THEME_LIGHT if self.current_theme == "light" else THEME_DARK
        global C
        C.clear()
        C.update(theme_palette)

        # Re-apply TTK styles
        self._ttk_styles()

        # Recursive traverser to update all child widgets
        def retheme_widget(w):
            if hasattr(w, "retheme"):
                w.retheme()
            else:
                bg_key = getattr(w, "theme_bg", None)
                fg_key = getattr(w, "theme_fg", None)
                
                config_kwargs = {}
                if bg_key and bg_key in C:
                    config_kwargs["bg"] = C[bg_key]
                if fg_key and fg_key in C:
                    config_kwargs["fg"] = C[fg_key]
                
                if config_kwargs:
                    try:
                        w.config(**config_kwargs)
                    except Exception:
                        pass
                
                # Special widget adjustments
                if isinstance(w, tk.Button) and not hasattr(w, "retheme"):
                    if w == self.btn_proc:
                        w.config(bg=C["btn_primary"], fg=C["bg"],
                                 activebackground=C["btn_primary_h"], activeforeground=C["bg"])
                elif isinstance(w, tk.Entry) and not hasattr(w, "retheme"):
                    try:
                        w.config(bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"])
                    except Exception:
                        pass
                elif isinstance(w, ttk.Treeview):
                    try:
                        w.tag_configure("locked", foreground=C["locked_row"])
                        w.tag_configure("normal", foreground=C["text2"])
                    except Exception:
                        pass

            for child in w.winfo_children():
                retheme_widget(child)

        retheme_widget(self.root)

        # Treeview stillerini doğrudan widget seviyesinde de yenile (Windows uyumluluk garantisi)
        try:
            self.tree_saved.tag_configure("locked", foreground=C["locked_row"])
        except Exception:
            pass
        self.root.configure(bg=C["bg"])

    # LAYOUT
    def _build(self):
        self._build_statusbar()   # ÖNCE — her zaman altta
        self._build_toolbar()
        self._build_main()

    # ── Status bar ───────────────────────────────────────────────────────────
    def _build_statusbar(self):
        self.statusbar = tk.Frame(self.root, bg=C["statusbar_bg"])
        if self.show_status_bar:
            self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.statusbar.theme_bg = "statusbar_bg"

        div = tk.Frame(self.statusbar, bg=C["border"], height=1)
        div.pack(fill=tk.X)
        div.theme_bg = "border"

        row = tk.Frame(self.statusbar, bg=C["statusbar_bg"])
        row.pack(fill=tk.X, padx=16, pady=(5, 4))
        row.theme_bg = "statusbar_bg"

        self.lbl_log = tk.Label(
            row, text="", bg=C["statusbar_bg"], fg=C["text_muted"],
            font=("Segoe UI", 9, "bold"), anchor=tk.W
        )
        self.lbl_log.pack(side=tk.LEFT)
        self.lbl_log.theme_bg = "statusbar_bg"
        self.lbl_log.theme_fg = "text_muted"

        self.lbl_percent = tk.Label(
            row, text="", bg=C["statusbar_bg"], fg=C["accent"],
            font=("Segoe UI", 9, "bold"), anchor=tk.W
        )
        self.lbl_percent.pack(side=tk.LEFT, padx=(5, 0))
        self.lbl_percent.theme_bg = "statusbar_bg"
        self.lbl_percent.theme_fg = "accent"

        self.progress = ModernProgressBar(self.statusbar)
        self.progress.pack(fill=tk.X)

    # ── Toolbar ──────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        tb = tk.Frame(self.root, bg=C["toolbar_bg"], height=64)
        tb.pack(side=tk.TOP, fill=tk.X)
        tb.pack_propagate(False)
        tb.theme_bg = "toolbar_bg"

        div_b = tk.Frame(tb, bg=C["border"], height=1)
        div_b.pack(side=tk.BOTTOM, fill=tk.X)
        div_b.theme_bg = "border"

        # Container to center all elements vertically
        cnt = tk.Frame(tb, bg=C["toolbar_bg"])
        cnt.pack(fill=tk.BOTH, expand=True, padx=20)
        cnt.theme_bg = "toolbar_bg"

        # ── Left Part: Logo ──
        self._load_logo(cnt)

        # Subtle vertical separator line
        div_v = tk.Frame(cnt, bg=C["border"], width=1)
        div_v.pack(side=tk.LEFT, fill=tk.Y, pady=14, padx=16)
        div_v.theme_bg = "border"

        # ── Middle Part: Process Button & Elevated Status Pill ──
        self.btn_proc = ModernButton(
            cnt, text="", style="primary", font_size=9,
            label_padx=16, label_pady=5,
            command=self._open_picker
        )
        self.btn_proc.pack(side=tk.LEFT, pady=14)

        # Elevated Status Pill Badge Container
        self.status_wrap = tk.Frame(cnt, bg=C["surface3"], padx=12, pady=6)
        self.status_wrap.pack(side=tk.LEFT, padx=16, pady=12)
        self.status_wrap.theme_bg = "surface3"

        self.lbl_status = tk.Label(
            self.status_wrap, text="",
            bg=C["surface3"], fg=C["text"],
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_status.pack(side=tk.LEFT)
        self.lbl_status.theme_bg = "surface3"
        self.lbl_status.theme_fg = "text"

        # ── Right Part: Controls (Language, Theme, Settings) ──
        right = tk.Frame(cnt, bg=C["toolbar_bg"])
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.theme_bg = "toolbar_bg"

        # Hidden theme toggle button to maintain backward-compatibility in _lang_update
        self.btn_theme = ModernButton(
            right, text="", style="default", font_size=8,
            label_padx=12, label_pady=5,
            command=self._toggle_theme
        )

        # Keep lbl_lang as an unpacked fallback widget to avoid breaking dynamic config translations
        self.lbl_lang = tk.Label(
            right, text="", bg=C["toolbar_bg"], fg=C["text_muted"],
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_lang.theme_bg = "toolbar_bg"
        self.lbl_lang.theme_fg = "text_muted"

        # Language dropdown combo
        self.cmb_lang = ModernCombo(right, values=["Türkçe", "English"], state="readonly", width=9)
        self.cmb_lang.set("Türkçe")
        self.cmb_lang.pack(side=tk.LEFT, padx=(0, 12), pady=14)
        self.cmb_lang.bind("<<ComboboxSelected>>", self._on_lang_change)

        # Settings button
        self.btn_settings = ModernButton(
            right, text="", style="default", font_size=8,
            label_padx=12, label_pady=5,
            command=self._open_settings_dialog
        )
        self.btn_settings.pack(side=tk.LEFT, pady=14)

        # Keep btn_about as a hidden backward-compatible mock to prevent AttributeErrors in _lang_update
        self.btn_about = tk.Frame(right)
        self.btn_about.set_text = lambda text: None

    def _load_logo(self, parent):
        """Logo görselini tipografik (yazı) olarak yükle (Renk ve boyut değiştirmeden)."""
        logo_frame = tk.Frame(parent, bg=C["toolbar_bg"])
        logo_frame.pack(side=tk.LEFT, padx=(16, 6), pady=10)
        logo_frame.theme_bg = "toolbar_bg"

        lbl_logo = tk.Label(
            logo_frame, text="SPEXRON ENGINE",
            font=("Segoe UI", 13, "bold"),
            bg=C["toolbar_bg"], fg="#FFD700"
        )
        lbl_logo.pack(side=tk.LEFT)
        lbl_logo.theme_bg = "toolbar_bg"

    # ── Ana içerik ────────────────────────────────────────────────────────────
    def _build_main(self):
        # Üst yarı: Found | Scanner
        top = tk.Frame(self.root, bg=C["bg"])
        top.pack(fill=tk.BOTH, expand=True)
        top.theme_bg = "bg"

        self._build_found_panel(top)
        
        div_mid = tk.Frame(top, bg=C["border"], width=1)
        div_mid.pack(side=tk.LEFT, fill=tk.Y)
        div_mid.theme_bg = "border"

        self._build_scanner_panel(top)

        # Ayırıcı
        div_bot = tk.Frame(self.root, bg=C["border"], height=1)
        div_bot.pack(fill=tk.X)
        div_bot.theme_bg = "border"

        # Cheat table
        self._build_cheat_panel()

    # ── Found Addresses ───────────────────────────────────────────────────────
    def _build_found_panel(self, parent):
        wrap = tk.Frame(parent, bg=C["bg"])
        wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        wrap.theme_bg = "bg"

        # Panel header (Clean modern title)
        hdr = tk.Frame(wrap, bg=C["surface2"], pady=0)
        hdr.pack(fill=tk.X, side=tk.TOP)
        hdr.theme_bg = "surface2"

        # Left accent stripe (Fluent Blue for Found panel)
        div_acc = tk.Frame(hdr, bg=C["accent"], width=3)
        div_acc.pack(side=tk.LEFT, fill=tk.Y)
        div_acc.theme_bg = "accent"

        self.lbl_found_title = tk.Label(hdr, text="  FOUND ADDRESSES",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), pady=10
                 )
        self.lbl_found_title.pack(side=tk.LEFT)
        self.lbl_found_title.theme_bg = "surface2"
        self.lbl_found_title.theme_fg = "text"

        # Capsule Badge for count label
        self._found_badge = tk.Frame(hdr, bg=C["bg"], padx=8, pady=2)
        self._found_badge.pack(side=tk.RIGHT, padx=12)
        self._found_badge.theme_bg = "bg"

        self._found_lbl = tk.Label(self._found_badge, text="",
                                   bg=C["bg"], fg=C["accent"],
                                   font=("Segoe UI", 8, "bold"))
        self._found_lbl.pack()
        self._found_lbl.theme_bg = "bg"
        self._found_lbl.theme_fg = "accent"

        div_sub = tk.Frame(wrap, bg=C["border"], height=1)
        div_sub.pack(fill=tk.X, side=tk.TOP)
        div_sub.theme_bg = "border"

        # Footer hint & Down arrow button (Packed side=tk.BOTTOM FIRST)
        footer_row = tk.Frame(wrap, bg=C["bg"])
        footer_row.pack(fill=tk.X, side=tk.BOTTOM, ipady=4)
        footer_row.theme_bg = "bg"

        self.btn_add_selected = ModernButton(
            footer_row, text="  ⬇  ", style="primary", font_size=8,
            label_padx=10, label_pady=4,
            command=self._add_selected_to_cheat_table
        )
        self.btn_add_selected.pack(side=tk.RIGHT, padx=8, pady=2)

        # Separator between Treeview and Footer
        div_foot = tk.Frame(wrap, bg=C["border"], height=1)
        div_foot.pack(fill=tk.X, side=tk.BOTTOM)
        div_foot.theme_bg = "border"

        # Treeview (Packed in the remaining TOP space with expand=True)
        tv = tk.Frame(wrap, bg=C["surface"])
        tv.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        tv.theme_bg = "surface"

        cols = ("Address", "Value")
        self.tree_found = ttk.Treeview(
            tv, columns=cols, show="headings",
            style="Treeview")
        self.tree_found.heading("Address", text="ADDRESS")
        self.tree_found.heading("Value",   text="VALUE")
        self.tree_found.column("Address", width=180, anchor=tk.CENTER, minwidth=140)
        self.tree_found.column("Value",   width=120, anchor=tk.CENTER, minwidth=80)
        
        # Dinamik Scrollbar (Cheat Engine tarzı)
        vsb = AutoScrollbar(tv, orient=tk.VERTICAL,
                             command=self.tree_found.yview,
                             style="Modern.Vertical.TScrollbar"
                             )
        self.tree_found.configure(yscrollcommand=vsb.set)
        self.tree_found.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_found.bind("<Double-1>", self._add_to_cheat_table)
        self.tree_found.bind("<Button-3>", self._on_found_rightclick)



    # ── Scanner Panel ─────────────────────────────────────────────────────────
    def _build_scanner_panel(self, parent):
        wrap = tk.Frame(parent, bg=C["bg"], width=340)
        wrap.pack(side=tk.RIGHT, fill=tk.Y)
        wrap.pack_propagate(False)
        wrap.theme_bg = "bg"

        # Header (Clean modern title)
        hdr = tk.Frame(wrap, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        hdr.theme_bg = "surface2"

        # Left accent stripe (Fluent Blue for Scanner panel)
        div_acc = tk.Frame(hdr, bg=C["accent"], width=3)
        div_acc.pack(side=tk.LEFT, fill=tk.Y)
        div_acc.theme_bg = "accent"

        self.lbl_scanner_title = tk.Label(hdr, text="  SCANNER",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), pady=10
                 )
        self.lbl_scanner_title.pack(side=tk.LEFT)
        self.lbl_scanner_title.theme_bg = "surface2"
        self.lbl_scanner_title.theme_fg = "text"

        div_sub = tk.Frame(wrap, bg=C["border"], height=1)
        div_sub.pack(fill=tk.X)
        div_sub.theme_bg = "border"

        # Compact elevated card envelope for form inputs
        card_wrap = tk.Frame(wrap, bg=C["border"], padx=1, pady=1)
        card_wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        card_wrap.theme_bg = "border"

        body = tk.Frame(card_wrap, bg=C["surface"], padx=12, pady=6)
        body.pack(fill=tk.BOTH, expand=True)
        body.theme_bg = "surface"

        def field_label(text):
            lbl = tk.Label(body, text=text, bg=C["surface"], fg=C["text_muted"],
                     font=("Segoe UI", 8, "bold"),
                     anchor=tk.W)
            lbl.pack(fill=tk.X, pady=(0, 2))
            lbl.theme_bg = "surface"
            lbl.theme_fg = "text_muted"

        # 1. ARANACAK DEĞER (Value) - Cheat Engine düzeni gereği en üstte
        field_label("")  # placeholder for lang update
        self.lbl_sv = body.winfo_children()[-1]
        self._ent_wrap = tk.Frame(body, bg=C["border"], padx=1, pady=1)
        self._ent_wrap.pack(fill=tk.X, pady=(0, 4))
        self._ent_wrap.theme_bg = "border"

        self.ent_val = tk.Entry(
            self._ent_wrap, bg=C["entry_bg"], fg=C["text"],
            insertbackground=C["accent"],
            font=("Consolas", 11), relief=tk.FLAT)
        self.ent_val.pack(fill=tk.X, ipady=4)
        self.ent_val.bind("<FocusIn>",
                          lambda _: self._ent_wrap.config(bg=C["accent"]))
        self.ent_val.bind("<FocusOut>",
                          lambda _: self._ent_wrap.config(bg=C["border"]))

        # 2. ARAMA TİPİ (Scan Type)
        field_label("")  # placeholder for lang update
        self.lbl_st = body.winfo_children()[-1]
        self.cmb_scan_type = ModernCombo(
            body, values=[], state="readonly",
            style="TCombobox")
        self.cmb_scan_type.pack(fill=tk.X, pady=(0, 4))
        self.cmb_scan_type.bind("<<ComboboxSelected>>", self._on_scan_type_change)

        # 3. DEĞER TİPİ (Value Type)
        field_label("")
        self.lbl_vt = body.winfo_children()[-1]
        self.cmb_val_type = ModernCombo(
            body, values=[],
            state="readonly", style="TCombobox")
        self.cmb_val_type.pack(fill=tk.X, pady=(0, 4))

        # Separator inside the card
        div_btn = tk.Frame(body, bg=C["border"], height=1)
        div_btn.pack(fill=tk.X, pady=4)
        div_btn.theme_bg = "border"

        # Buttons Grid (FIRST & NEXT yan yana - dikey alan kazanmak ve çakışmayı önlemek için!)
        btn_grid = tk.Frame(body, bg=C["surface"])
        btn_grid.pack(fill=tk.X, pady=(0, 4))
        btn_grid.theme_bg = "surface"

        self.btn_first = ModernButton(
            btn_grid, text="FIRST SCAN", style="primary",
            command=self._start_first_scan)
        self.btn_first.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))

        self.btn_next = ModernButton(
            btn_grid, text="NEXT SCAN", style="default",
            command=self._start_next_scan)
        self.btn_next.disable()
        self.btn_next.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))

        self.btn_reset = ModernButton(
            body, text="NEW SCAN / RESET", style="danger",
            command=self._reset_scan)
        self.btn_reset.pack(fill=tk.X)

        # Speedhack section container frame
        sh_container = tk.Frame(body, bg=C["surface"], bd=0)
        sh_container.pack(fill=tk.X, pady=(16, 0))
        sh_container.theme_bg = "surface"

        # Divider separating buttons and speedhack
        div_sh = tk.Frame(sh_container, bg=C["border"], height=1)
        div_sh.pack(fill=tk.X, pady=(0, 10))
        div_sh.theme_bg = "border"

        # Row 1: Checkbox & Entry + OK Button
        sh_top_row = tk.Frame(sh_container, bg=C["surface"])
        sh_top_row.pack(fill=tk.X, pady=(0, 8))
        sh_top_row.theme_bg = "surface"

        self._main_sh_var = tk.BooleanVar(value=self.speedhack_enabled)
        self.chk_main_sh = tk.Checkbutton(
            sh_top_row, text="Speedhack", variable=self._main_sh_var,
            bg=C["surface"], fg=C["text"], selectcolor=C["surface2"],
            activebackground=C["surface"], activeforeground=C["accent"],
            font=("Segoe UI", 9, "bold"), command=self._on_main_speedhack_toggle
        )
        self.chk_main_sh.pack(side=tk.LEFT)

        # Right aligned group for Entry & OK button
        sh_right_group = tk.Frame(sh_top_row, bg=C["surface"])
        sh_right_group.pack(side=tk.RIGHT)
        sh_right_group.theme_bg = "surface"

        self._ent_sh_val_wrap = tk.Frame(sh_right_group, bg=C["border"], padx=1, pady=1)
        self._ent_sh_val_wrap.pack(side=tk.LEFT, padx=(0, 6))
        self._ent_sh_val_wrap.theme_bg = "border"

        self.ent_main_sh_val = tk.Entry(
            self._ent_sh_val_wrap, bg=C["entry_bg"], fg=C["text"],
            insertbackground=C["accent"], width=6, font=("Consolas", 10, "bold"),
            relief=tk.FLAT, justify=tk.CENTER
        )
        self.ent_main_sh_val.pack(side=tk.LEFT, ipady=3)
        self.ent_main_sh_val.insert(0, self.speedhack_speed)
        
        self.ent_main_sh_val.bind("<FocusIn>", lambda _: self._ent_sh_val_wrap.config(bg=C["accent"]))
        self.ent_main_sh_val.bind("<FocusOut>", lambda _: self._ent_sh_val_wrap.config(bg=C["border"]))
        self.ent_main_sh_val.bind("<Return>", lambda _: self._apply_main_speedhack())

        self.btn_apply_sh = ModernButton(
            sh_right_group, text="OK", style="primary", font_size=8,
            command=self._apply_main_speedhack, label_padx=10, label_pady=4
        )
        self.btn_apply_sh.pack(side=tk.LEFT)

        # Row 2: Slider with min/max labels
        sh_slider_row = tk.Frame(sh_container, bg=C["surface"])
        sh_slider_row.pack(fill=tk.X, pady=(2, 4))
        sh_slider_row.theme_bg = "surface"

        self.lbl_sh_min = tk.Label(
            sh_slider_row, text="x0.0", bg=C["surface"], fg=C["text_muted"],
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_sh_min.pack(side=tk.LEFT, padx=(0, 6))
        self.lbl_sh_min.theme_bg = "surface"
        self.lbl_sh_min.theme_fg = "text_muted"

        # Modern flat custom canvas slider
        self.sh_scale = ModernSlider(
            sh_slider_row, from_=0.0, to=500.0, command=self._on_scale_change
        )
        self.sh_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.sh_scale.set(float(self.speedhack_speed))

        self.lbl_sh_max = tk.Label(
            sh_slider_row, text="x500.0", bg=C["surface"], fg=C["text_muted"],
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_sh_max.pack(side=tk.LEFT, padx=(6, 0))
        self.lbl_sh_max.theme_bg = "surface"
        self.lbl_sh_max.theme_fg = "text_muted"

    # ── Cheat Table ───────────────────────────────────────────────────────────
    def _build_cheat_panel(self):
        wrap = tk.Frame(self.root, bg=C["bg"])
        wrap.pack(fill=tk.BOTH, expand=True)
        wrap.theme_bg = "bg"

        hdr = tk.Frame(wrap, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        hdr.theme_bg = "surface2"

        div_acc = tk.Frame(hdr, bg=C["gold"], width=3)
        div_acc.pack(side=tk.LEFT, fill=tk.Y)
        div_acc.theme_bg = "gold"

        self.lbl_cheat_title = tk.Label(hdr, text="  CHEAT TABLE",
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), pady=10
                 )
        self.lbl_cheat_title.pack(side=tk.LEFT)
        self.lbl_cheat_title.theme_bg = "surface2"
        self.lbl_cheat_title.theme_fg = "text"

        # Add Manual Button
        self.btn_add_manual = ModernButton(
            hdr, text="", style="accent", font_size=8,
            label_padx=10, label_pady=4,
            command=self._open_manual_add_dialog
        )
        self.btn_add_manual.pack(side=tk.RIGHT, padx=8, pady=4)

        # Capsule Badge for cheat count label
        self._cheat_badge = tk.Frame(hdr, bg=C["bg"], padx=8, pady=2)
        self._cheat_badge.pack(side=tk.RIGHT, padx=4)
        self._cheat_badge.theme_bg = "bg"

        self._cheat_lbl = tk.Label(self._cheat_badge, text="",
                                   bg=C["bg"], fg=C["gold"],
                                   font=("Segoe UI", 8, "bold"))
        self._cheat_lbl.pack()
        self._cheat_lbl.theme_bg = "bg"
        self._cheat_lbl.theme_fg = "gold"

        div_sub = tk.Frame(wrap, bg=C["border_sub"], height=1)
        div_sub.pack(fill=tk.X)
        div_sub.theme_bg = "border_sub"

        tv = tk.Frame(wrap, bg=C["surface"])
        tv.pack(fill=tk.BOTH, expand=True)
        tv.theme_bg = "surface"

        cols = ("Active", "Description", "Address", "Type", "Value")
        self.tree_saved = ttk.Treeview(
            tv, columns=cols, show="headings",
            style="Treeview", height=6)
        self.tree_saved.column("Active",      width=110, anchor=tk.CENTER, stretch=False, minwidth=90)
        self.tree_saved.column("Description", width=300, anchor=tk.W,      minwidth=120)
        self.tree_saved.column("Address",     width=180, anchor=tk.CENTER, stretch=False, minwidth=140)
        self.tree_saved.column("Type",        width=90,  anchor=tk.CENTER, stretch=False, minwidth=70)
        self.tree_saved.column("Value",       width=140, anchor=tk.CENTER, minwidth=80)

        vsb = ttk.Scrollbar(tv, orient=tk.VERTICAL,
                             command=self.tree_saved.yview,
                             style="Modern.Vertical.TScrollbar"
                             )
        self.tree_saved.configure(yscrollcommand=vsb.set)
        self.tree_saved.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Tag'ları widget oluşturulduktan hemen sonra tanımla
        self.tree_saved.tag_configure("locked", foreground=C["locked_row"])

        self.tree_saved.bind("<Double-1>", self._on_cheat_dblclick)
        self.tree_saved.bind("<Button-1>", self._on_cheat_click)
        self.tree_saved.bind("<Button-3>", self._on_cheat_rightclick)
        self.tree_saved.bind("<Delete>",   self._on_cheat_delete_key)
        self.tree_saved.bind("<space>",    self._on_cheat_space_key)

        # End of cheat panel build

    # ═══════════════════════════════════════════════════════════════════════
    # DİL
    # ═══════════════════════════════════════════════════════════════════════
    def _on_lang_change(self, _=None):
        self.current_lang = "tr" if self.cmb_lang.get() == "Türkçe" else "en"
        self._lang_update()

    def _lang_update(self):
        # Toolbar
        if self.scanner and self.target_pid:
            pn = self.current_process_name or "?"
            self.lbl_status.config(
                text=f"  ●  {pn}  ·  PID {self.target_pid}",
                fg=C["green"])
            self.btn_proc.set_text(self.t("btn_connected", pn, self.target_pid))
        else:
            self.lbl_status.config(
                text=f"  ○  {self.t('status_disconnected')}",
                fg=C["text_muted"])
            self.btn_proc.set_text(self.t("btn_select_process"))

        # Treeview headings
        self.tree_found.heading("Address", text=self.t("tree_col_address").upper())
        self.tree_found.heading("Value",   text=self.t("tree_col_value").upper())
        self.tree_saved.heading("Active",      text=self.t("tree_col_active").upper())
        self.tree_saved.heading("Description", text=self.t("tree_col_description").upper())
        self.tree_saved.heading("Address",     text=self.t("tree_col_saved_address").upper())
        self.tree_saved.heading("Type",        text=self.t("tree_col_saved_type").upper())
        self.tree_saved.heading("Value",       text=self.t("tree_col_saved_value").upper())

        # Scanner labels with premium icons
        self.lbl_st.config(text=f"⚙  {self.t('lbl_scan_type').upper()}")
        self.lbl_vt.config(text=f"📊  {self.t('lbl_val_type').upper()}")
        self.lbl_sv.config(text=f"🔍  {self.t('lbl_search_val').upper()}")
        self.lbl_lang.config(text=self.t("lang_label"))

        # Translate Value Type combobox options!
        vt_opts = [self.t(k) for k in ("val_1byte", "val_2bytes", "val_4bytes", "val_8bytes", "val_float", "val_double")]
        cur_vt_idx = self.cmb_val_type.current()
        self.cmb_val_type.configure(values=vt_opts)
        if 0 <= cur_vt_idx < len(vt_opts):
            self.cmb_val_type.current(cur_vt_idx)
        else:
            self.cmb_val_type.set(self.t("val_4bytes"))

        # Buttons
        self.btn_first.set_text(self.t("btn_first_scan").upper())
        self.btn_next.set_text(self.t("btn_next_scan").upper())
        self.btn_reset.set_text(self.t("btn_reset").upper())
        self.btn_add_manual.set_text(self.t("btn_add_manual").upper())

        # Translate theme toggle button
        theme_key = "theme_dark" if self.current_theme == "light" else "theme_light"
        self.btn_theme.set_text(self.t(theme_key))

        # Translate settings button
        self.btn_settings.set_text(self.t("btn_settings").upper())

        # Translate about button
        self.btn_about.set_text(self.t("btn_about").upper())

        # Combobox options
        is_next = self.btn_next._enabled
        if is_next:
            opts = [self.t(k) for k in (
                "scan_exact","scan_bigger","scan_smaller","scan_between",
                "scan_increased","scan_decreased","scan_changed","scan_unchanged")]
        else:
            opts = [self.t(k) for k in (
                "scan_exact","scan_bigger","scan_smaller","scan_between","scan_unknown")]
        idx = self.cmb_scan_type.current()
        self.cmb_scan_type.configure(values=opts)
        if 0 <= idx < len(opts):
            self.cmb_scan_type.current(idx)
        else:
            self.cmb_scan_type.set(self.t("scan_exact"))

        # Placeholder check
        all_ram = (LOCALIZATION["tr"]["all_ram_scan"],
                   LOCALIZATION["en"]["all_ram_scan"])
        if self.ent_val.get() in all_ram:
            self.ent_val.config(state=tk.NORMAL)
            self.ent_val.delete(0, tk.END)
            self.ent_val.insert(0, self.t("all_ram_scan"))
            self.ent_val.config(state=tk.DISABLED)

        # Title labels translation
        self.lbl_found_title.config(text=f"  {self.t('lbl_found_addresses')}")
        self.lbl_scanner_title.config(text=f"  {self.t('lbl_scanner')}")
        self.lbl_cheat_title.config(text=f"  {self.t('lbl_cheat_table')}")

        self.log(self.t("log_idle"), C["text_muted"])
        self._refresh_found_lbl()
        self._refresh_cheat_tree()

    def _refresh_found_lbl(self):
        if not self.scanner:
            self._found_lbl.config(text=self.t("lbl_results_zero"))
            return
        total = len(self.scanner.found_addresses)
        self._found_lbl.config(text=self.t("lbl_results_count", total, ""))

    # ═══════════════════════════════════════════════════════════════════════
    # LOG
    # ═══════════════════════════════════════════════════════════════════════
    def log(self, text, color=None):
        self.lbl_log.config(text=f"  {text}", fg=color or C["text_muted"])

    # ═══════════════════════════════════════════════════════════════════════
    # PROCESS
    # ═══════════════════════════════════════════════════════════════════════
    def _open_picker(self):
        ProcessPickerDialog(self.root, self._attach, self.current_lang, LOCALIZATION, theme_palette=C)

    def _open_settings_dialog(self):
        SettingsDialog(self)

    def _open_about_dialog(self):
        messagebox.showinfo(
            "Spexron Engine v2.0",
            "SPEXRON tarafından kodlanmıştır.\nCoded by SPEXRON.",
            parent=self.root
        )

    def _open_pointer_scanner(self, target_addr):
        PointerScannerDialog(self, target_addr)

    def _resolve_pointer(self, addr_str):
        """
        Dinamik pointer offset zincirlerini çözer.
        Örnek formatlar:
        - "0x7FFE103B->0x14->0x30"
        - "client.dll+0x2FA8C->0x10->0x8"
        """
        if not self.scanner:
            return None
        parts = addr_str.strip().split("->")
        base_part = parts[0]
        base_addr = None
        if "+" in base_part:
            try:
                mod_name, offset_str = base_part.split("+", 1)
                mod_base = self.scanner.get_module_base(mod_name.strip())
                if mod_base is None:
                    return None
                offset = int(offset_str.strip(), 16) if offset_str.strip().lower().startswith("0x") else int(offset_str.strip())
                base_addr = mod_base + offset
            except Exception:
                return None
        else:
            try:
                base_addr = int(base_part, 16) if base_part.lower().startswith("0x") else int(base_part)
            except Exception:
                return None
        curr_addr = base_addr
        for offset_str in parts[1:]:
            val = self.scanner.read_memory(curr_addr, "8 Bytes")
            if val is None:
                return None
            try:
                offset = int(offset_str.strip(), 16) if offset_str.strip().lower().startswith("0x") else int(offset_str.strip())
                curr_addr = val + offset
            except Exception:
                return None
        return curr_addr

    def _live_update_tick(self):
        if not self.lock_thread_active:
            return
        if self.scanner:
            for addr_str, info in list(self.saved_cheats.items()):
                real_addr = self._resolve_pointer(addr_str) if "->" in addr_str else None
                if "->" in addr_str and real_addr is None:
                    continue
                target_addr = real_addr if real_addr is not None else int(addr_str, 16)
                live_val = self.scanner.read_memory(target_addr, info["type"])
                if live_val is not None:
                    info["value"] = str(live_val)
            for item in self.tree_saved.get_children():
                vals = self.tree_saved.item(item, "values")
                addr_str = vals[2]
                if addr_str in self.saved_cheats:
                    info = self.saved_cheats[addr_str]
                    lock_txt = (self.t("tree_active_locked")
                                if info["locked"]
                                else self.t("tree_active_unlocked"))
                    self.tree_saved.item(item, values=(
                        lock_txt, info["description"],
                        addr_str, self._translate_val_type(info["type"]), info["value"]
                    ))
        self.root.after(500, self._live_update_tick)

    def _on_found_rightclick(self, event):
        item = self.tree_found.identify_row(event.y)
        if not item:
            return
        current_selection = self.tree_found.selection()
        if item not in current_selection:
            self.tree_found.selection_set(item)
        addr = self.tree_found.item(item, "values")[0]
        FoundContextMenu(self, addr).tk_popup(event.x_root, event.y_root)

    def _apply_settings_to_scanner(self):
        if not self.scanner:
            return
        try:
            start_addr = int(self.scan_start_addr, 16)
            self.scanner.min_addr = start_addr
        except Exception:
            pass
        try:
            end_addr = int(self.scan_end_addr, 16)
            self.scanner.max_addr = end_addr
        except Exception:
            pass
        self.scanner.scan_mem_private = self.scan_mem_private
        self.scanner.scan_mem_image   = self.scan_mem_image
        self.scanner.scan_mem_mapped  = self.scan_mem_mapped
        self.scanner.scan_writable_only = self.scan_writable_only
        self.scanner.scan_mem_executable = self.scan_mem_executable
        self.scanner.scan_mem_copy_on_write = self.scan_mem_copy_on_write

    def _attach(self, pid, process_name):
        try:
            self.target_pid           = pid
            self.current_process_name = process_name
            self.scanner              = MemoryScanner(pid)
            self._apply_settings_to_scanner()
            self.lbl_status.config(
                text=f"  ●  {process_name}  ·  PID {pid}", fg=C["green"])
            self.btn_proc.set_text(self.t("btn_connected", process_name, pid))
            self.log(self.t("log_hook_established", process_name, pid), C["green"])
        except Exception as e:
            messagebox.showerror("Spexron Engine", str(e))
            self.lbl_status.config(
                text=f"  ✕  {self.t('status_disconnected')}", fg=C["red"])

    # ═══════════════════════════════════════════════════════════════════════
    # SCAN TYPE
    # ═══════════════════════════════════════════════════════════════════════
    def _on_scan_type_change(self, _=None):
        st = self.cmb_scan_type.get()
        unknown_labels = (LOCALIZATION["tr"]["scan_unknown"],
                          LOCALIZATION["en"]["scan_unknown"])
        if st in unknown_labels:
            self.ent_val.config(state=tk.NORMAL)
            self.ent_val.delete(0, tk.END)
            self.ent_val.insert(0, self.t("all_ram_scan"))
            self.ent_val.config(state=tk.DISABLED)
        else:
            self.ent_val.config(state=tk.NORMAL)
            cur = self.ent_val.get()
            all_ram = (LOCALIZATION["tr"]["all_ram_scan"],
                       LOCALIZATION["en"]["all_ram_scan"])
            if cur in all_ram:
                self.ent_val.delete(0, tk.END)

    # ═══════════════════════════════════════════════════════════════════════
    # FIRST SCAN
    # ═══════════════════════════════════════════════════════════════════════
    def _start_first_scan(self):
        if not self.scanner:
            messagebox.showerror("Spexron", self.t("log_access_denied"))
            return
        st_label = self.cmb_scan_type.get()
        st = _build_scan_map(LOCALIZATION, self.current_lang).get(
            st_label, MemoryScanner.ST_EXACT)
        vt_label = self.cmb_val_type.get()
        vt = _build_val_type_map(LOCALIZATION, self.current_lang).get(vt_label, "4 Bytes")
        val_str = self.ent_val.get().strip()
        if not val_str and st != MemoryScanner.ST_UNKNOWN:
            messagebox.showwarning("Spexron", self.t("log_specify_val"))
            
            return
        self.btn_first.disable()
        self.btn_next.disable()
        self.progress["value"] = 0
        self.lbl_percent.config(text="0%")
        self.log(self.t("log_scan_initiated"), C["accent"])
        threading.Thread(
            target=self._run_first_scan, args=(st, vt, val_str), daemon=True
        ).start()

    def _run_first_scan(self, st, vt, val_str):
        t0 = time.time()
        def _prog(p, snapshot):
            self.root.after(0, lambda: (
                self.progress.configure(value=p),
                self.lbl_percent.config(text=f"{p}%"),
                self._update_found_tree_dynamic(snapshot)))
        count   = self.scanner.first_scan(st, vt, val_str, progress_callback=_prog)
        elapsed = time.time() - t0
        self.root.after(0, lambda: self._finish_first_scan(count, elapsed))

    def _update_found_tree_dynamic(self, snapshot):
        for item in self.tree_found.get_children():
            self.tree_found.delete(item)
        for addr, val in snapshot:
            self.tree_found.insert("", tk.END, values=(f"0x{addr:016X}", val))
        self._refresh_found_lbl()

    def _finish_first_scan(self, count, elapsed):
        self.progress["value"] = 100
        self.lbl_percent.config(text="")
        self.btn_first.enable()
        self.btn_next.enable()
        opts = [self.t(k) for k in (
            "scan_exact","scan_bigger","scan_smaller","scan_between",
            "scan_increased","scan_decreased","scan_changed","scan_unchanged")]
        self.cmb_scan_type.configure(values=opts)
        self.cmb_scan_type.set(self.t("scan_exact"))
        self._fill_found_tree()
        color = C["green"] if count > 0 else C["red"]
        self.log(self.t("log_scan_finished", elapsed, count), color)

    # ═══════════════════════════════════════════════════════════════════════
    # NEXT SCAN
    # ═══════════════════════════════════════════════════════════════════════
    def _start_next_scan(self):
        if not self.scanner or not self.scanner.found_addresses:
            return
        st = _build_scan_map(LOCALIZATION, self.current_lang).get(
            self.cmb_scan_type.get(), MemoryScanner.ST_EXACT)
        vt_label = self.cmb_val_type.get()
        vt = _build_val_type_map(LOCALIZATION, self.current_lang).get(vt_label, "4 Bytes")
        val_str = self.ent_val.get().strip()
        self.log(self.t("log_refining"), C["accent"])
        count = self.scanner.next_scan(st, vt, val_str)
        self._fill_found_tree()
        self.log(self.t("log_refined_finished", count),
                 C["green"] if count > 0 else C["red"])

    # ═══════════════════════════════════════════════════════════════════════
    # RESET
    # ═══════════════════════════════════════════════════════════════════════
    def _reset_scan(self):
        if self.scanner:
            self.scanner.found_addresses = {}
        self._fill_found_tree()
        self.saved_cheats = {}
        self._refresh_cheat_tree()
        self.progress["value"] = 0
        self.lbl_percent.config(text="")
        self.btn_next.disable()
        opts = [self.t(k) for k in (
            "scan_exact","scan_bigger","scan_smaller","scan_between","scan_unknown")]
        self.cmb_scan_type.configure(values=opts)
        self.cmb_scan_type.set(self.t("scan_exact"))
        self.ent_val.config(state=tk.NORMAL)
        self.ent_val.delete(0, tk.END)
        self.log(self.t("log_reset"))

    # ═══════════════════════════════════════════════════════════════════════
    # FOUND TREE
    # ═══════════════════════════════════════════════════════════════════════
    def _fill_found_tree(self):
        for item in self.tree_found.get_children():
            self.tree_found.delete(item)
        if not self.scanner:
            self._refresh_found_lbl()
            return
        vt_label = self.cmb_val_type.get()
        vt = _build_val_type_map(LOCALIZATION, self.current_lang).get(vt_label, "4 Bytes")
        total = len(self.scanner.found_addresses)
        limit = min(250, total)
        for addr in list(self.scanner.found_addresses.keys())[:limit]:
            val = self.scanner.read_memory(addr, vt)
            if val is not None:
                self.scanner.found_addresses[addr] = val
                self.tree_found.insert("", tk.END,
                    values=(f"0x{addr:016X}", val))
        self._refresh_found_lbl()

    # ═══════════════════════════════════════════════════════════════════════
    # CHEAT TABLE
    # ═══════════════════════════════════════════════════════════════════════
    def _add_to_cheat_table(self, _=None):
        self._add_selected_to_cheat_table()

    def _add_selected_to_cheat_table(self):
        sel = self.tree_found.selection()
        if not sel:
            return
        vt_label = self.cmb_val_type.get()
        vt = _build_val_type_map(LOCALIZATION, self.current_lang).get(vt_label, "4 Bytes")
        added_count = 0
        for item in sel:
            addr_hex, val_str = self.tree_found.item(item, "values")
            try:
                key = f"0x{int(addr_hex, 16):016X}"
            except Exception:
                key = addr_hex
            if key in self.saved_cheats:
                continue
            self.saved_cheats[key] = {
                "description": self.t("desc_default"),
                "type":  vt,
                "value": val_str,
                "locked": False,
            }
            added_count += 1
        if added_count > 0:
            self._refresh_cheat_tree()
            if added_count == 1:
                addr_hex, _ = self.tree_found.item(sel[0], "values")
                self.log(self.t("log_record_added", addr_hex), C["gold"])
            else:
                self.log(self.t("log_records_added_multi", added_count), C["gold"])

    def _refresh_cheat_tree(self):
        for item in self.tree_saved.get_children():
            self.tree_saved.delete(item)
        for addr, info in self.saved_cheats.items():
            lock_txt = (self.t("tree_active_locked")
                        if info["locked"]
                        else self.t("tree_active_unlocked"))
            tags = ("locked",) if info["locked"] else ()
            self.tree_saved.insert("", tk.END, tags=tags,
                values=(lock_txt, info["description"],
                        addr, self._translate_val_type(info["type"]), info["value"]))
        self.tree_saved.tag_configure("locked", foreground=C["locked_row"])
        self._cheat_lbl.config(text=self.t("lbl_entries_count", len(self.saved_cheats)))

    def _on_cheat_click(self, event):
        region = self.tree_saved.identify("region", event.x, event.y)
        col    = self.tree_saved.identify_column(event.x)
        item   = self.tree_saved.identify_row(event.y)
        if region != "cell" or not item or col != "#1":
            return
        addr = self.tree_saved.item(item, "values")[2]
        if addr in self.saved_cheats:
            self.saved_cheats[addr]["locked"] = not self.saved_cheats[addr]["locked"]
            self._refresh_cheat_tree()
            self.log(self.t("log_freeze_active", addr), C["gold"])

    def _on_cheat_dblclick(self, event):
        region = self.tree_saved.identify("region", event.x, event.y)
        col    = self.tree_saved.identify_column(event.x)
        item   = self.tree_saved.identify_row(event.y)
        if region != "cell" or not item:
            return
        addr = self.tree_saved.item(item, "values")[2]
        if addr not in self.saved_cheats:
            return
        info = self.saved_cheats[addr]
        if col == "#2":
            self._ctx_edit_desc(addr, info)
        elif col == "#4":
            self._ctx_edit_type(addr, info)
        elif col == "#5":
            self._show_value_editor(addr, info)
        elif col == "#1":
            self.saved_cheats[addr]["locked"] = not info["locked"]
            self._refresh_cheat_tree()

    def _on_cheat_rightclick(self, event):
        item = self.tree_saved.identify_row(event.y)
        if not item:
            return
        current_selection = self.tree_saved.selection()
        if item not in current_selection:
            self.tree_saved.selection_set(item)
        addr = self.tree_saved.item(item, "values")[2]
        if addr in self.saved_cheats:
            CheatContextMenu(self, addr, self.saved_cheats[addr]
                             ).tk_popup(event.x_root, event.y_root)

    # ── Context aksiyonları ───────────────────────────────────────────────────
    def _show_value_editor(self, addr, info):
        ValueEditorDialog(self, addr, info)

    def _open_manual_add_dialog(self):
        ManualAddDialog(self)

    def _on_cheat_delete_key(self, event=None):
        sel = self.tree_saved.selection()
        if not sel:
            return
        for item in sel:
            addr = self.tree_saved.item(item, "values")[2]
            if addr in self.saved_cheats:
                del self.saved_cheats[addr]
        self._refresh_cheat_tree()
        self.log(self.t("log_records_deleted_multi", len(sel)), C["red"])

    def _on_cheat_space_key(self, event=None):
        sel = self.tree_saved.selection()
        if not sel:
            return
        any_unlocked = any(not self.saved_cheats[self.tree_saved.item(i, "values")[2]]["locked"] for i in sel if self.tree_saved.item(i, "values")[2] in self.saved_cheats)
        target_state = any_unlocked
        for item in sel:
            addr = self.tree_saved.item(item, "values")[2]
            if addr in self.saved_cheats:
                self.saved_cheats[addr]["locked"] = target_state
        self._refresh_cheat_tree()
        self.log(self.t("log_records_frozen_multi", len(sel), "✔" if target_state else "—"), C["gold"])

    def _ctx_set_value(self, addr, info):
        sel = self.tree_saved.selection()
        selected_addrs = []
        for item in sel:
            vals = self.tree_saved.item(item, "values")
            if vals:
                selected_addrs.append(vals[2])
        if addr not in selected_addrs:
            selected_addrs.append(addr)

        prompt_text = self.t("set_val_prompt", f"{len(selected_addrs)} {self.t('lbl_entries_count').strip()}") if len(selected_addrs) > 1 else self.t("set_val_prompt", addr)

        val = simpledialog.askstring(
            self.t("set_val_title"),
            prompt_text,
            initialvalue=str(info["value"]), parent=self.root)

        if val is not None:
            success_count = 0
            for a in selected_addrs:
                if a in self.saved_cheats:
                    inf = self.saved_cheats[a]
                    self.saved_cheats[a]["value"] = val
                    if self.scanner:
                        try:
                            target_addr = self._resolve_pointer(a) if "->" in a else int(a, 16)
                            if target_addr is not None:
                                ok = self.scanner.write_memory(target_addr, val, inf["type"])
                                if ok:
                                    success_count += 1
                        except Exception:
                            pass
            if len(selected_addrs) > 1:
                self.log(f"{success_count} adet adrese toplu sabit deger yazildi.", C["gold"])
            else:
                self.log(self.t("log_writeprocessmemory", addr, val), C["green"] if success_count > 0 else C["red"])
            self._refresh_cheat_tree()

    def _ctx_toggle_freeze(self, addr, state):
        if addr in self.saved_cheats:
            self.saved_cheats[addr]["locked"] = state
            self._refresh_cheat_tree()
            self.log(self.t("log_freeze_active", addr), C["gold"])

    def _ctx_edit_desc(self, addr, info):
        v = simpledialog.askstring(self.t("desc_dialog_title"),
                                   self.t("desc_dialog_prompt"),
                                   initialvalue=info["description"],
                                   parent=self.root)
        if v is not None:
            self.saved_cheats[addr]["description"] = v
            self._refresh_cheat_tree()

    def _ctx_edit_type(self, addr, info):
        v = simpledialog.askstring(self.t("type_dialog_title"),
                                   self.t("type_dialog_prompt"),
                                   initialvalue=info["type"],
                                   parent=self.root)
        if v in ("1 Byte","2 Bytes","4 Bytes","8 Bytes","Float","Double"):
            self.saved_cheats[addr]["type"] = v
            self._refresh_cheat_tree()

    def _ctx_remove(self, addr):
        if addr in self.saved_cheats:
            del self.saved_cheats[addr]
            self._refresh_cheat_tree()

    # ═══════════════════════════════════════════════════════════════════════
    # FREEZE LOOP
    # ═══════════════════════════════════════════════════════════════════════
    def _freezer_loop(self):
        while self.lock_thread_active:
            if self.scanner:
                for addr_str, info in list(self.saved_cheats.items()):
                    if info["locked"]:
                        try:
                            target_addr = self._resolve_pointer(addr_str) if "->" in addr_str else int(addr_str, 16)
                            if target_addr is not None:
                                self.scanner.write_memory(
                                    target_addr, info["value"], info["type"])
                        except Exception:
                            pass
            time.sleep(self.freeze_interval)

    def __del__(self):
        self.lock_thread_active = False


# ─────────────────────────────────────────────────────────────────────────────
# GÖSTERGE TARAYICI DİYALOĞU
# ─────────────────────────────────────────────────────────────────────────────
    def _parse_hotkey_to_tk(self, hk_str):
        hk_str = hk_str.strip().lower()
        if not hk_str:
            return None
        parts = hk_str.split('+')
        tk_parts = []
        for part in parts:
            part = part.strip()
            if part == "ctrl":
                tk_parts.append("Control")
            elif part == "alt":
                tk_parts.append("Alt")
            elif part == "shift":
                tk_parts.append("Shift")
            elif part == "space":
                tk_parts.append("space")
            elif part == "enter":
                tk_parts.append("Return")
            else:
                if len(part) == 1:
                    tk_parts.append(part)
                else:
                    tk_parts.append(part.capitalize())
        
        if len(tk_parts) == 1:
            return f"<{tk_parts[0]}>"
        else:
            return f"<{'-'.join(tk_parts)}>"

    def _bind_hotkeys(self):
        if not hasattr(self, "_active_hotkey_bindings"):
            self._active_hotkey_bindings = {}
            
        for seq in list(self._active_hotkey_bindings.keys()):
            try:
                self.root.unbind(seq)
            except Exception:
                pass
        self._active_hotkey_bindings.clear()

        def on_select_proc(event=None):
            self._open_process_picker()

        def on_pause_proc(event=None):
            self.log("Süreç askıya alındı / devam ettirildi (Simüle edildi).", C["gold"])

        def on_freeze_addr(event=None):
            self._on_cheat_space_key()

        def on_speedhack(event=None):
            self._toggle_speedhack_hotkey()

        def on_next_scan(event=None):
            self._start_next_scan()

        def on_reset_scan(event=None):
            self._reset_scan()

        bindings = [
            (self.hotkey_select_proc, on_select_proc),
            (self.hotkey_pause_proc, on_pause_proc),
            (self.hotkey_freeze_addr, on_freeze_addr),
            (self.hotkey_speedhack, on_speedhack),
            (self.hotkey_next_scan, on_next_scan),
            (self.hotkey_reset_scan, on_reset_scan),
        ]

        for hk_str, cb in bindings:
            seq = self._parse_hotkey_to_tk(hk_str)
            if seq:
                self.root.bind(seq, cb)
                self._active_hotkey_bindings[seq] = cb

    def _on_scale_change(self, val):
        formatted_val = f"{float(val):.1f}"
        self.ent_main_sh_val.delete(0, tk.END)
        self.ent_main_sh_val.insert(0, formatted_val)
        if self.speedhack_enabled:
            self._apply_main_speedhack(silent=True)

    def _on_main_speedhack_toggle(self):
        self.speedhack_enabled = self._main_sh_var.get()
        if self.speedhack_enabled:
            self._apply_main_speedhack()
        else:
            self.speedhack_speed = "1.0"
            self.ent_main_sh_val.delete(0, tk.END)
            self.ent_main_sh_val.insert(0, "1.0")
            try:
                if abs(float(self.sh_scale.get()) - 1.0) > 0.01:
                    self.sh_scale.set(1.0)
            except Exception:
                pass

    def _apply_main_speedhack(self, silent=False):
        new_speed = self.ent_main_sh_val.get().strip()
        try:
            val = float(new_speed)
            self.speedhack_speed = new_speed
            self.speedhack_enabled = True
            self._main_sh_var.set(True)
            try:
                if abs(float(self.sh_scale.get()) - val) > 0.01:
                    self.sh_scale.set(val)
            except Exception:
                pass
            if not silent:
                self.log(f"Speedhack etkinleştirildi: {val}x", C["green"])
        except ValueError:
            if not silent:
                messagebox.showerror("Spexron", "Geçersiz hız değeri!")
            self._main_sh_var.set(False)
            self.speedhack_enabled = False

    def _toggle_speedhack_hotkey(self):
        self.speedhack_enabled = not self.speedhack_enabled
        self._main_sh_var.set(self.speedhack_enabled)
        if self.speedhack_enabled:
            self._apply_main_speedhack()
        else:
            self._on_main_speedhack_toggle()


class PointerScannerDialog(tk.Toplevel):
    def __init__(self, gui, target_address_str):
        super().__init__(gui.root)
        self._gui = gui
        self._target_address_str = target_address_str

        self.title(gui.t("ptr_title"))
        self.geometry("540x520")
        self.configure(bg=C["bg"])
        self.transient(gui.root)
        self.grab_set()

        self._build()
        self._center()

    def _build(self):
        g = self._gui
        # Header
        hdr = tk.Frame(self, bg=C["surface2"])
        hdr.pack(fill=tk.X)
        tk.Frame(hdr, bg=C["accent"], width=3).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(hdr, text=g.t("ptr_header"),
                 bg=C["surface2"], fg=C["text"],
                 font=("Segoe UI", 11, "bold"), pady=12
                 ).pack(side=tk.LEFT)
        tk.Frame(self, bg=C["border_sub"], height=1).pack(fill=tk.X)

        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=12)

        # Config row
        config_f = tk.Frame(body, bg=C["bg"])
        config_f.pack(fill=tk.X, pady=5)
        config_f.columnconfigure(1, weight=1)

        # Target Address
        tk.Label(config_f, text=g.t("ptr_lbl_target"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self._ent_target = tk.Entry(config_f, bg=C["entry_bg"], fg=C["text"], insertbackground=C["accent"],
                                    font=("Consolas", 10), relief=tk.FLAT, highlightthickness=1,
                                    highlightbackground=C["border"], highlightcolor=C["accent"])
        self._ent_target.grid(row=0, column=1, sticky=tk.EW, padx=(12, 0), pady=5, ipady=4)
        self._ent_target.insert(0, self._target_address_str)

        # Max Offset
        tk.Label(config_f, text=g.t("ptr_lbl_max_offset"), bg=C["bg"], fg=C["text_muted"],
                 font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self._cmb_offset = ModernCombo(config_f, values=["0x400", "0x1000", "0x4000", "0x10000"], state="readonly", style="TCombobox")
        self._cmb_offset.grid(row=1, column=1, sticky=tk.EW, padx=(12, 0), pady=5)
        self._cmb_offset.set("0x1000")

        # Static Modules Only Checkbox
        self._static_var = tk.BooleanVar(value=True)
        tk.Checkbutton(config_f, text=g.t("ptr_chk_static_only"),
                       variable=self._static_var, bg=C["bg"], fg=C["text"],
                       selectcolor=C["surface2"], activebackground=C["bg"],
                       activeforeground=C["accent"], font=("Segoe UI", 9)
                       ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=6)

        # Scan Button
        self.btn_scan = ModernButton(
            body, text=g.t("ptr_btn_scan"), style="primary",
            command=self._start_scan
        )
        self.btn_scan.pack(fill=tk.X, pady=8)

        # Progress bar
        self.progress_frame = tk.Frame(body, bg=C["bg"])
        self.progress_frame.pack(fill=tk.X, pady=4)
        self.progress = ModernProgressBar(self.progress_frame)
        self.progress.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # Treeview list
        lst = tk.Frame(body, bg=C["bg"])
        lst.pack(fill=tk.BOTH, expand=True, pady=8)

        cols = ("Offset", "LiveValue")
        self._tree = ttk.Treeview(lst, columns=cols, show="tree headings", style="Treeview")
        self._tree.heading("#0",   text=g.t("ptr_col_path"))
        self._tree.heading("Offset",  text=g.t("ptr_col_offset"))
        self._tree.heading("LiveValue", text=g.t("ptr_col_value"))
        self._tree.column("#0",    width=280, anchor=tk.W)
        self._tree.column("Offset",   width=100, anchor=tk.CENTER, stretch=False)
        self._tree.column("LiveValue",  width=100, anchor=tk.CENTER, stretch=False)

        vsb = ttk.Scrollbar(lst, orient=tk.VERTICAL, command=self._tree.yview, style="Modern.Vertical.TScrollbar")
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree.bind("<Double-1>", self._on_double_click)

        # Label count
        self.lbl_count = tk.Label(body, text=g.t("ptr_lbl_count", 0),
                                  bg=C["bg"], fg=C["text_muted"], font=("Segoe UI", 8))
        self.lbl_count.pack(anchor=tk.W)

    def _start_scan(self):
        if not self._gui.scanner:
            messagebox.showerror(self._gui.t("manual_dialog_title"), self._gui.t("ptr_err_no_process"), parent=self)
            return

        target_str = self._ent_target.get().strip()
        try:
            target_addr = int(target_str, 16) if target_str.lower().startswith("0x") else int(target_str)
        except Exception:
            messagebox.showerror(self._gui.t("manual_dialog_title"), self._gui.t("ptr_err_invalid_addr"), parent=self)
            return

        max_offset_str = self._cmb_offset.get()
        try:
            max_offset = int(max_offset_str, 16) if max_offset_str.lower().startswith("0x") else int(max_offset_str)
        except Exception:
            max_offset = 4096

        self.btn_scan.disable()
        self.progress["value"] = 0

        # Run scan inside a background thread so the GUI does not freeze!
        threading.Thread(target=self._run_scan, args=(target_addr, max_offset), daemon=True).start()

    def _run_scan(self, target_addr, max_offset):
        g = self._gui
        
        def _prog(pct):
            self.root.after(0, lambda: self.progress.configure(value=pct))

        # Perform actual low-level pointer scan
        raw_pointers = g.scanner.scan_for_pointers(target_addr, max_offset, progress_callback=_prog)
        
        # Resolve loaded modules to find relative paths
        modules = g.scanner.get_loaded_modules()
        
        # Populate results list
        self.root.after(0, lambda: self._fill_results(raw_pointers, modules))

    def _fill_results(self, pointers, modules):
        # Clear tree
        for item in self._tree.get_children():
            self._tree.delete(item)

        static_only = self._static_var.get()
        count = 0
        g = self._gui

        for ptr_addr, offset in pointers:
            # Map address relative to module base if possible
            mod_rel = self._get_module_relative_path(ptr_addr, modules)
            if static_only and not mod_rel:
                continue

            path_str = mod_rel if mod_rel else f"0x{ptr_addr:X}"
            full_pointer_path = f"{path_str}->0x{offset:X}"
            
            # Read live value of resolved pointer
            live_val = "N/A"
            if g.scanner:
                real_addr = g._resolve_pointer(full_pointer_path)
                if real_addr is not None:
                    # Let's read standard 4 Bytes value as dynamic indicator
                    val = g.scanner.read_memory(real_addr, "4 Bytes")
                    if val is not None:
                        live_val = str(val)

            self._tree.insert("", tk.END, text=path_str, values=(f"+0x{offset:X}", live_val))
            count += 1

        self.lbl_count.config(text=g.t("ptr_lbl_count", count))
        self.btn_scan.enable()
        self.progress["value"] = 100

    def _get_module_relative_path(self, ptr_addr, modules):
        for name, base, size in modules:
            if base <= ptr_addr < base + size:
                offset = ptr_addr - base
                return f"{name}+0x{offset:X}"
        return None

    def _on_double_click(self, event):
        sel = self._tree.selection()
        if not sel:
            return
        item = sel[0]
        base_path = self._tree.item(item, "text")
        offset = self._tree.item(item, "values")[0].replace("+", "")
        
        full_pointer_path = f"{base_path}->{offset}"
        
        # Add to cheat table!
        g = self._gui
        if full_pointer_path in g.saved_cheats:
            return
            
        g.saved_cheats[full_pointer_path] = {
            "description": g.t("ptr_col_path"),
            "type":  "4 Bytes",
            "value": self._tree.item(item, "values")[1],
            "locked": False,
        }
        g._refresh_cheat_tree()
        g.log(g.t("ptr_log_added", full_pointer_path), C["gold"])
        self.destroy()

    def _center(self):
        self.update_idletasks()
        r = self._gui.root
        x = r.winfo_x() + (r.winfo_width()  - self.winfo_width())  // 2
        y = r.winfo_y() + (r.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
