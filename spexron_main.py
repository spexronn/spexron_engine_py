# ==========================================
# SPEXRON ENGINE v2.0 - GİRİŞ NOKTASI
# Bu dosyayı doğrudan çalıştırın veya run.bat kullanın
# ==========================================

import sys
import os

# Dosyanın bulunduğu dizini Python yoluna ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import tkinter as tk
from spexron_gui import SpexronEngineGUI


def main():
    root = tk.Tk()

    # ── Pencere ikonu (varsa) ──────────────────────────────────────────────
    icon_paths = [
        os.path.join(BASE_DIR, "SPEXRON.png"),
        os.path.join(BASE_DIR, "SPEXRON (1).png"),
    ]
    for path in icon_paths:
        try:
            img = tk.PhotoImage(file=path)
            root.iconphoto(True, img)
            break
        except Exception:
            pass

    app = SpexronEngineGUI(root)

    # ── Pencere kapatma handler'ı ─────────────────────────────────────────
    def on_close():
        app.lock_thread_active = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
