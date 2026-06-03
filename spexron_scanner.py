# ==========================================
# SPEXRON ENGINE v2.0 - MEMORY SCANNER CORE
# Windows API tabanlı 64-bit bellek tarama motoru
# ==========================================

import ctypes
from ctypes import wintypes
import struct
import time

# ── Windows API Sabitleri ──────────────────────────────────────────────────────
PROCESS_ALL_ACCESS  = 0x1F0FFF
MEM_COMMIT          = 0x1000
PAGE_READWRITE      = 0x04
TH32CS_SNAPPROCESS  = 0x00000002

kernel32 = ctypes.windll.kernel32


class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture",  wintypes.WORD),
        ("wReserved",               wintypes.WORD),
        ("dwPageSize",              wintypes.DWORD),
        ("lpMinimumApplicationAddress", ctypes.c_void_p),
        ("lpMaximumApplicationAddress", ctypes.c_void_p),
        ("dwActiveProcessorMask",   ctypes.c_void_p),
        ("dwNumberOfProcessors",    wintypes.DWORD),
        ("dwProcessorType",         wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel",         wintypes.WORD),
        ("wProcessorRevision",      wintypes.WORD),
    ]


class MEMORY_BASIC_INFORMATION64(ctypes.Structure):
    _fields_ = [
        ("BaseAddress",       ctypes.c_ulonglong),
        ("AllocationBase",    ctypes.c_ulonglong),
        ("AllocationProtect", ctypes.c_ulong),
        ("alignment1",        ctypes.c_ulong),
        ("RegionSize",        ctypes.c_ulonglong),
        ("State",             ctypes.c_ulong),
        ("Protect",           ctypes.c_ulong),
        ("Type",              ctypes.c_ulong),
        ("alignment2",        ctypes.c_ulong),
    ]


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",              wintypes.DWORD),
        ("cntUsage",            wintypes.DWORD),
        ("th32ProcessID",       wintypes.DWORD),
        ("th32DefaultHeapID",   ctypes.c_void_p),
        ("th32ModuleID",        wintypes.DWORD),
        ("cntThreads",          wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase",      wintypes.LONG),
        ("dwFlags",             wintypes.DWORD),
        ("szExeFile",           ctypes.c_char * 260),
    ]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.c_void_p),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HANDLE),
        ("szModule",           ctypes.c_char * 256),
        ("szExePath",          ctypes.c_char * 260),
    ]


kernel32.Module32First.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
kernel32.Module32First.restype = wintypes.BOOL
kernel32.Module32Next.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
kernel32.Module32Next.restype = wintypes.BOOL

kernel32.VirtualProtectEx.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_size_t,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD)
]
kernel32.VirtualProtectEx.restype = wintypes.BOOL


# ── Yardımcı: Süreç Listesi ───────────────────────────────────────────────────

def enumerate_processes():
    """Sistemdeki tüm çalışan süreçleri (PID, ad) çiftleri olarak döndürür."""
    hSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if hSnap == -1:
        return []
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if not kernel32.Process32First(hSnap, ctypes.byref(pe32)):
        kernel32.CloseHandle(hSnap)
        return []
    procs = []
    while True:
        name = pe32.szExeFile.decode("utf-8", errors="ignore")
        if name:
            procs.append((pe32.th32ProcessID, name))
        if not kernel32.Process32Next(hSnap, ctypes.byref(pe32)):
            break
    kernel32.CloseHandle(hSnap)
    procs.sort(key=lambda x: x[1].lower())
    return procs


def find_pid_by_name(process_name):
    """Adı verilen sürecin ilk PID'ini döndürür; yoksa None."""
    for pid, name in enumerate_processes():
        if name.lower() == process_name.lower():
            return pid
    return None


# ── Tarama Motoru ─────────────────────────────────────────────────────────────

class MemoryScanner:
    """
    Hibrit 64-bit bellek tarayıcısı.
    VirtualQueryEx ile adres uzayını yürüyerek ReadProcessMemory ile okur.
    """

    VALUE_TYPES = {
        "1 Byte":   (1, "<b"),
        "2 Bytes":  (2, "<h"),
        "4 Bytes":  (4, "<i"),
        "8 Bytes":  (8, "<q"),
        "Float":    (4, "<f"),
        "Double":   (8, "<d"),
    }

    # Dahili scan-type sabit etiketleri (UI dilinden bağımsız)
    ST_EXACT     = "EXACT"
    ST_BIGGER    = "BIGGER"
    ST_SMALLER   = "SMALLER"
    ST_BETWEEN   = "BETWEEN"
    ST_UNKNOWN   = "UNKNOWN"
    ST_INCREASED = "INCREASED"
    ST_DECREASED = "DECREASED"
    ST_CHANGED   = "CHANGED"
    ST_UNCHANGED = "UNCHANGED"

    def __init__(self, pid):
        self.pid = pid
        self.process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        self.found_addresses = {}   # {address: last_known_value}

        sys_info = SYSTEM_INFO()
        kernel32.GetSystemInfo(ctypes.byref(sys_info))
        self.min_addr = sys_info.lpMinimumApplicationAddress or 0x10000
        self.max_addr = sys_info.lpMaximumApplicationAddress or 0x7FFFFFFFFFFF

        # Advanced Cheat Engine-like page scanning configuration
        self.scan_mem_private = True
        self.scan_mem_image   = True
        self.scan_mem_mapped  = False
        self.scan_writable_only = True
        self.scan_mem_executable = False
        self.scan_mem_copy_on_write = False

    def _is_scanable_region(self, mbi):
        # State must be MEM_COMMIT (0x1000)
        if mbi.State != 0x1000:
            return False
            
        # Check Type (Private = 0x20000, Image = 0x1000000, Mapped = 0x40000)
        type_ok = False
        if mbi.Type == 0x20000 and self.scan_mem_private:
            type_ok = True
        elif mbi.Type == 0x1000000 and self.scan_mem_image:
            type_ok = True
        elif mbi.Type == 0x40000 and self.scan_mem_mapped:
            type_ok = True
            
        if not type_ok:
            return False
            
        # Check Protection dynamically based on settings
        # PAGE_READONLY = 0x02, PAGE_READWRITE = 0x04, PAGE_WRITECOPY = 0x08
        # PAGE_EXECUTE = 0x10, PAGE_EXECUTE_READ = 0x20, PAGE_EXECUTE_READWRITE = 0x40, PAGE_EXECUTE_WRITECOPY = 0x80
        allowed = 0x04 | 0x40 # basic writeable
        if not self.scan_writable_only:
            allowed |= 0x02 | 0x20
        if self.scan_mem_copy_on_write:
            allowed |= 0x08 | 0x80
        if self.scan_mem_executable:
            allowed |= 0x10 | 0x20 | 0x40 | 0x80
            
        return bool(mbi.Protect & allowed)

    def __del__(self):
        if hasattr(self, "process_handle") and self.process_handle:
            kernel32.CloseHandle(self.process_handle)

    # ── Düşük seviye okuma / yazma ────────────────────────────────────────────

    def _type_info(self, val_type):
        return self.VALUE_TYPES.get(val_type, (4, "<i"))

    def read_memory(self, address, val_type):
        size, fmt = self._type_info(val_type)
        buf = ctypes.create_string_buffer(size)
        n   = ctypes.c_size_t(0)
        ok  = kernel32.ReadProcessMemory(
            self.process_handle, ctypes.c_void_p(address), buf, size, ctypes.byref(n)
        )
        if ok and n.value == size:
            return struct.unpack(fmt, buf.raw[:size])[0]
        return None

    def write_memory(self, address, value, val_type):
        size, fmt = self._type_info(val_type)
        try:
            if val_type in ("Float", "Double"):
                typed = float(value)
            else:
                # Modulo wrap integers to avoid struct.pack overflow exceptions
                typed = int(value)
                if val_type == "1 Byte":
                    typed = (typed + 128) % 256 - 128
                elif val_type == "2 Bytes":
                    typed = (typed + 32768) % 65536 - 32768
                elif val_type == "4 Bytes":
                    typed = (typed + 2147483648) % 4294967296 - 2147483648
                elif val_type == "8 Bytes":
                    typed = (typed + 9223372036854775808) % 18446744073709551616 - 9223372036854775808
            data  = struct.pack(fmt, typed)
        except Exception:
            return False
            
        old_protect = wintypes.DWORD(0)
        # Temporarily make page writable (PAGE_EXECUTE_READWRITE = 0x40)
        kernel32.VirtualProtectEx(
            self.process_handle, ctypes.c_void_p(address), size, 0x40, ctypes.byref(old_protect)
        )
        
        n  = ctypes.c_size_t(0)
        ok = kernel32.WriteProcessMemory(
            self.process_handle, ctypes.c_void_p(address), data, size, ctypes.byref(n)
        )
        
        # Restore original protection
        if old_protect.value:
            temp = wintypes.DWORD(0)
            kernel32.VirtualProtectEx(
                self.process_handle, ctypes.c_void_p(address), size, old_protect.value, ctypes.byref(temp)
            )
            
        return bool(ok and n.value == size)

    # ── İlk Tarama ────────────────────────────────────────────────────────────

    def first_scan(self, scan_type, val_type, value_str, progress_callback=None):
        """
        scan_type: ST_* sabitlerinden biri
        Bulgu sözlüğünü (found_addresses) doldurur; eşleşen adres sayısını döndürür.
        """
        self.found_addresses = {}
        size, fmt = self._type_info(val_type)
        is_float  = val_type in ("Float", "Double")
        conv      = float if is_float else int

        v1 = v2 = None
        if scan_type != self.ST_UNKNOWN:
            try:
                parts = value_str.split("-") if "-" in value_str else [value_str]
                v1 = conv(parts[0])
                v2 = conv(parts[1]) if len(parts) > 1 else None
            except Exception:
                return 0

        # Fast dry run with VirtualQueryEx to discover total committed scan range
        regions = []
        mbi = MEMORY_BASIC_INFORMATION64()
        address = self.min_addr
        while address < self.max_addr:
            res = kernel32.VirtualQueryEx(
                self.process_handle, ctypes.c_void_p(address),
                ctypes.byref(mbi), ctypes.sizeof(mbi)
            )
            if not res:
                break
            if self._is_scanable_region(mbi):
                regions.append((mbi.BaseAddress, mbi.RegionSize))
            address = mbi.BaseAddress + mbi.RegionSize

        total_bytes = sum(size for _, size in regions)
        if total_bytes == 0:
            return 0

        bytes_scanned = 0
        last_callback_time = 0

        for base_addr, reg_size in regions:
            buf = ctypes.create_string_buffer(reg_size)
            n = ctypes.c_size_t(0)
            ok = kernel32.ReadProcessMemory(
                self.process_handle, ctypes.c_void_p(base_addr),
                buf, reg_size, ctypes.byref(n)
            )
            if ok and n.value > 0:
                data = buf.raw[:n.value]
                for offset in range(0, len(data) - size, size):
                    val = struct.unpack_from(fmt, data, offset)[0]
                    if self._match_first(scan_type, val, v1, v2):
                        self.found_addresses[base_addr + offset] = val

            bytes_scanned += reg_size

            # Rate limit the callback updates to every 50ms to prevent GUI locking
            curr_time = time.time()
            if progress_callback and (curr_time - last_callback_time > 0.05 or bytes_scanned == total_bytes):
                pct = min(100, int((bytes_scanned / total_bytes) * 100))
                snapshot = list(self.found_addresses.items())[:250]
                progress_callback(pct, snapshot)
                last_callback_time = curr_time

        return len(self.found_addresses)

    def _match_first(self, st, val, v1, v2):
        if st == self.ST_EXACT:     return val == v1
        if st == self.ST_BIGGER:    return val > v1
        if st == self.ST_SMALLER:   return val < v1
        if st == self.ST_BETWEEN:   return (v1 <= val <= v2) if v2 is not None else val == v1
        if st == self.ST_UNKNOWN:   return True
        return False

    # ── Sonraki Tarama ────────────────────────────────────────────────────────

    def next_scan(self, scan_type, val_type, value_str):
        is_float = val_type in ("Float", "Double")
        conv     = float if is_float else int

        v1 = v2 = None
        if scan_type not in (self.ST_INCREASED, self.ST_DECREASED,
                              self.ST_CHANGED,   self.ST_UNCHANGED):
            try:
                parts = value_str.split("-") if "-" in value_str else [value_str]
                v1 = conv(parts[0])
                v2 = conv(parts[1]) if len(parts) > 1 else None
            except Exception:
                return len(self.found_addresses)

        refined = {}
        for addr, prev_val in list(self.found_addresses.items()):
            curr = self.read_memory(addr, val_type)
            if curr is None:
                continue
            if self._match_next(scan_type, curr, prev_val, v1, v2):
                refined[addr] = curr

        self.found_addresses = refined
        return len(self.found_addresses)

    def _match_next(self, st, curr, prev, v1, v2):
        if st == self.ST_EXACT:     return curr == v1
        if st == self.ST_BIGGER:    return curr > v1
        if st == self.ST_SMALLER:   return curr < v1
        if st == self.ST_BETWEEN:   return (v1 <= curr <= v2) if v2 is not None else curr == v1
        if st == self.ST_INCREASED: return curr > prev
        if st == self.ST_DECREASED: return curr < prev
        if st == self.ST_CHANGED:   return curr != prev
        if st == self.ST_UNCHANGED: return curr == prev
        return False

    def get_module_base(self, module_name):
        """Dinamik olarak yüklenmiş DLL veya ana exe modülünün taban adresini döndürür."""
        hSnap = kernel32.CreateToolhelp32Snapshot(0x00000008 | 0x00000010, self.pid)
        if hSnap == -1:
            return None
        me32 = MODULEENTRY32()
        me32.dwSize = ctypes.sizeof(MODULEENTRY32)
        if not kernel32.Module32First(hSnap, ctypes.byref(me32)):
            kernel32.CloseHandle(hSnap)
            return None
            
        target = module_name.lower().strip()
        while True:
            curr_name = me32.szModule.decode("utf-8", errors="ignore").lower().strip()
            if curr_name == target or (target.endswith(".exe") and curr_name == target) or curr_name.endswith(target):
                base = me32.modBaseAddr
                kernel32.CloseHandle(hSnap)
                return base
            if not kernel32.Module32Next(hSnap, ctypes.byref(me32)):
                break
        kernel32.CloseHandle(hSnap)
        return None

    def get_loaded_modules(self):
        """Süreç tarafından yüklenen tüm DLL ve EXE modüllerini (ad, taban, boyut) olarak döndürür."""
        hSnap = kernel32.CreateToolhelp32Snapshot(0x00000008 | 0x00000010, self.pid)
        if hSnap == -1:
            return []
        me32 = MODULEENTRY32()
        me32.dwSize = ctypes.sizeof(MODULEENTRY32)
        if not kernel32.Module32First(hSnap, ctypes.byref(me32)):
            kernel32.CloseHandle(hSnap)
            return []
        modules = []
        while True:
            name = me32.szModule.decode("utf-8", errors="ignore")
            base = me32.modBaseAddr
            size = me32.modBaseSize
            if name:
                modules.append((name, base, size))
            if not kernel32.Module32Next(hSnap, ctypes.byref(me32)):
                break
        kernel32.CloseHandle(hSnap)
        return modules

    def scan_for_pointers(self, target_address, max_offset=4096, progress_callback=None):
        """
        Gelişmiş Gösterge/Offset Tarayıcı (Cheat Engine tarzı Pointer Scanner)
        Tüm committed bellek bölgelerini tarar ve target_address'e işaret eden statik veya dinamik gösterge yollarını bulur.
        """
        results = []
        
        regions = []
        mbi = MEMORY_BASIC_INFORMATION64()
        address = self.min_addr
        while address < self.max_addr:
            res = kernel32.VirtualQueryEx(
                self.process_handle, ctypes.c_void_p(address),
                ctypes.byref(mbi), ctypes.sizeof(mbi)
            )
            if not res:
                break
            if self._is_scanable_region(mbi):
                regions.append((mbi.BaseAddress, mbi.RegionSize))
            address = mbi.BaseAddress + mbi.RegionSize
            
        total_regions = len(regions)
        if total_regions == 0:
            return []
            
        ptr_size = 8
        fmt = "<Q"
        
        for idx, (base_addr, reg_size) in enumerate(regions):
            buf = ctypes.create_string_buffer(reg_size)
            n = ctypes.c_size_t(0)
            ok = kernel32.ReadProcessMemory(
                self.process_handle, ctypes.c_void_p(base_addr),
                buf, reg_size, ctypes.byref(n)
            )
            if ok and n.value > 0:
                data = buf.raw[:n.value]
                for offset in range(0, len(data) - ptr_size, 8):
                    val = struct.unpack_from(fmt, data, offset)[0]
                    if target_address - max_offset <= val <= target_address:
                        ptr_diff = target_address - val
                        results.append((base_addr + offset, ptr_diff))
                        
            if progress_callback and idx % 5 == 0:
                pct = int(((idx + 1) / total_regions) * 100)
                progress_callback(pct)
                
        return results
