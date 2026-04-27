import tkinter as tk
from tkinter import font as tkfont
from threading import Thread
import time
import math

# IMPORTS
from voice import speak, listen
from my_commands import execute_command
from ai_brain import ask_ai
from chat_memory import add_chat

# =========================
# COLORS — JARVIS HUD PALETTE
# =========================
BG_VOID      = "#020810"
BG_PANEL     = "#030c18"
BG_OVERLAY   = "#041020"
CYAN         = "#00d4ff"
CYAN_BRIGHT  = "#40eaff"
CYAN_DIM     = "#0a4a60"
CYAN_GHOST   = "#052030"
AMBER        = "#ffaa00"
RED_ALERT    = "#ff3344"
TEXT_CYAN    = "#7ad4f0"
TEXT_DIM     = "#2a6a8a"
TEXT_BRIGHT  = "#c0f0ff"
GRID_LINE    = "#051525"

# =========================
# ANIMATED RING CANVAS
# =========================
class HUDRing(tk.Canvas):
    def __init__(self, parent, size=120, **kwargs):
        super().__init__(parent, width=size, height=size,
                         bg=BG_VOID, highlightthickness=0, **kwargs)
        self.size = size
        self.cx = size // 2
        self.cy = size // 2
        self.angle = 0
        self.pulse = 0
        self.status_color = CYAN
        self._draw()
        self._animate()

    def _draw(self):
        self.delete("all")
        s = self.size
        cx, cy = self.cx, self.cy
        r = s * 0.42

        # Outer faint ring
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         outline=CYAN_DIM, width=1)

        # Middle dashed arc ring
        for i in range(24):
            a1 = math.radians(i * 15)
            a2 = math.radians(i * 15 + 10)
            x1 = cx + (r - 6) * math.cos(a1)
            y1 = cy - (r - 6) * math.sin(a1)
            x2 = cx + (r - 6) * math.cos(a2)
            y2 = cy - (r - 6) * math.sin(a2)
            self.create_line(x1, y1, x2, y2, fill=TEXT_DIM, width=1)

        # Spinning arc
        spin_start = self.angle % 360
        self.create_arc(cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4,
                        start=spin_start, extent=100,
                        outline=self.status_color, width=2, style="arc")
        self.create_arc(cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4,
                        start=spin_start + 180, extent=60,
                        outline=CYAN_DIM, width=1, style="arc")

        # Inner glow circle
        pulse_r = 14 + 3 * math.sin(self.pulse)
        self.create_oval(cx - pulse_r, cy - pulse_r,
                         cx + pulse_r, cy + pulse_r,
                         outline=self.status_color, width=1, fill=CYAN_GHOST)

        # Core dot
        dot = 5
        self.create_oval(cx - dot, cy - dot, cx + dot, cy + dot,
                         fill=self.status_color, outline="")

        # Cross-hair ticks
        tick_len = 8
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x1 = cx + (r + 4) * math.cos(rad)
            y1 = cy - (r + 4) * math.sin(rad)
            x2 = cx + (r + tick_len) * math.cos(rad)
            y2 = cy - (r + tick_len) * math.sin(rad)
            self.create_line(x1, y1, x2, y2, fill=self.status_color, width=1)

    def _animate(self):
        self.angle += 2
        self.pulse += 0.12
        self._draw()
        self.after(40, self._animate)

    def set_status_color(self, color):
        self.status_color = color


# =========================
# SCANLINE OVERLAY
# =========================
class ScanlineCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.bind("<Configure>", self._draw)

    def _draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        for y in range(0, h, 4):
            self.create_line(0, y, w, y, fill="#020c14", width=1)


# =========================
# APP CLASS
# =========================
class JarvisApp:
    def __init__(self):
        self.running = True
        self.status = "IDLE"

        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("960x620")
        self.root.configure(bg=BG_VOID)
        self.root.resizable(True, True)

        self._build_ui()
        self._greet()

        # Voice loop ENABLED
        Thread(target=self._voice_loop, daemon=True).start()
        self.root.mainloop()

    # =========================
    # UI BUILD
    # =========================
    def _build_ui(self):
        # ── TOP HEADER BAR ──────────────────────────────────────
        header = tk.Frame(self.root, bg=BG_VOID, height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Left accent stripe
        tk.Frame(header, bg=CYAN, width=3).pack(side="left", fill="y")

        # Logo / title block
        title_block = tk.Frame(header, bg=BG_VOID)
        title_block.pack(side="left", padx=16, pady=8)

        tk.Label(title_block, text="J.A.R.V.I.S.", bg=BG_VOID,
                 fg=CYAN, font=("Courier New", 18, "bold")).pack(anchor="w")
        tk.Label(title_block, text="Just A Rather Very Intelligent System",
                 bg=BG_VOID, fg=TEXT_DIM,
                 font=("Courier New", 7)).pack(anchor="w")

        # Status pill (right side)
        self.status_frame = tk.Frame(header, bg=BG_VOID)
        self.status_frame.pack(side="right", padx=20)
        self.status_dot = tk.Label(self.status_frame, text="●", bg=BG_VOID,
                                   fg=CYAN, font=("Courier New", 10))
        self.status_dot.pack(side="left")
        self.status_label = tk.Label(self.status_frame, text="IDLE",
                                     bg=BG_VOID, fg=TEXT_DIM,
                                     font=("Courier New", 10, "bold"))
        self.status_label.pack(side="left", padx=(4, 0))

        # Corner decorations
        tk.Label(header, text="SYS:OK  VER:3.1.4",
                 bg=BG_VOID, fg=CYAN_DIM,
                 font=("Courier New", 7)).pack(side="right", padx=10)

        # Horizontal separator
        tk.Frame(self.root, bg=CYAN_DIM, height=1).pack(fill="x")

        # ── MAIN BODY ────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG_VOID)
        body.pack(fill="both", expand=True)

        # ── LEFT PANEL (HUD + status) ────────────────────────────
        left = tk.Frame(body, bg=BG_PANEL, width=180)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Frame(left, bg=CYAN, height=1).pack(fill="x")

        # Ring widget
        ring_frame = tk.Frame(left, bg=BG_PANEL)
        ring_frame.pack(pady=(24, 8))
        self.hud_ring = HUDRing(ring_frame, size=130)
        self.hud_ring.pack()

        tk.Label(left, text="NEURAL CORE", bg=BG_PANEL,
                 fg=CYAN, font=("Courier New", 8, "bold")).pack()

        tk.Frame(left, bg=CYAN_DIM, height=1).pack(fill="x", padx=16, pady=12)

        # System metrics (static decorative)
        for label, val in [("CPU", "12%"), ("MEM", "48%"),
                            ("NET", "LIVE"), ("AI", "READY")]:
            row = tk.Frame(left, bg=BG_PANEL)
            row.pack(fill="x", padx=14, pady=2)
            tk.Label(row, text=label, bg=BG_PANEL, fg=TEXT_DIM,
                     font=("Courier New", 8)).pack(side="left")
            tk.Label(row, text=val, bg=BG_PANEL, fg=CYAN,
                     font=("Courier New", 8, "bold")).pack(side="right")

        tk.Frame(left, bg=CYAN_DIM, height=1).pack(fill="x", padx=16, pady=12)

        # Mode indicator
        self.mode_label = tk.Label(left, text="▶  STANDBY",
                                   bg=BG_PANEL, fg=AMBER,
                                   font=("Courier New", 8, "bold"))
        self.mode_label.pack()

        # Filler with bottom border
        tk.Frame(left, bg=BG_PANEL).pack(fill="both", expand=True)
        tk.Frame(left, bg=CYAN, height=1).pack(fill="x", side="bottom")

        # ── RIGHT CONTENT AREA ───────────────────────────────────
        right = tk.Frame(body, bg=BG_VOID)
        right.pack(side="left", fill="both", expand=True)

        # Thin top accent
        tk.Frame(right, bg=CYAN_DIM, height=1).pack(fill="x")

        # Chat header
        chat_header = tk.Frame(right, bg=BG_OVERLAY, height=28)
        chat_header.pack(fill="x")
        chat_header.pack_propagate(False)
        tk.Label(chat_header, text="  ◈  COMMUNICATION LOG",
                 bg=BG_OVERLAY, fg=TEXT_DIM,
                 font=("Courier New", 8, "bold")).pack(side="left", padx=8, pady=5)
        tk.Label(chat_header, text="ENCRYPTED  ⬤",
                 bg=BG_OVERLAY, fg=CYAN_DIM,
                 font=("Courier New", 7)).pack(side="right", padx=10, pady=5)

        # ── BOTTOM INPUT BAR (packed FIRST so expand=True chat doesn't eat it) ──
        tk.Frame(right, bg=CYAN_DIM, height=1).pack(side="bottom", fill="x")

        input_panel = tk.Frame(right, bg=BG_PANEL, height=60)
        input_panel.pack(side="bottom", fill="x")
        input_panel.pack_propagate(False)

        # Prompt symbol
        tk.Label(input_panel, text="⟩⟩",
                 bg=BG_PANEL, fg=CYAN,
                 font=("Courier New", 13, "bold")).pack(side="left", padx=(14, 4), pady=14)

        # Send button packed before entry (right-side anchor)
        send_btn = tk.Button(
            input_panel,
            text="TRANSMIT",
            command=self._send,
            bg=CYAN_GHOST,
            fg=CYAN,
            activebackground=CYAN_DIM,
            activeforeground=CYAN_BRIGHT,
            font=("Courier New", 9, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
        )
        send_btn.pack(side="right", padx=12, pady=14)

        # Text entry fills remaining width
        self.entry = tk.Entry(
            input_panel,
            bg=BG_PANEL,
            fg=CYAN_BRIGHT,
            insertbackground=CYAN_BRIGHT,
            font=("Courier New", 12),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightcolor=CYAN_DIM,
            highlightbackground=CYAN_GHOST,
            selectbackground=CYAN_DIM,
        )
        self.entry.pack(side="left", fill="both", expand=True, ipady=8, padx=(0, 8), pady=10)
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.focus()

        # ── CHAT AREA (packed AFTER input bar so it fills remaining space) ──
        chat_wrapper = tk.Frame(right, bg=BG_VOID)
        chat_wrapper.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(chat_wrapper, troughcolor=BG_PANEL,
                                 bg=CYAN_DIM, activebackground=CYAN,
                                 width=6, bd=0)
        scrollbar.pack(side="right", fill="y")

        self.chat_box = tk.Text(
            chat_wrapper,
            bg=BG_VOID,
            fg=TEXT_CYAN,
            font=("Courier New", 11),
            wrap="word",
            padx=16,
            pady=12,
            spacing1=3,
            spacing3=3,
            relief="flat",
            bd=0,
            yscrollcommand=scrollbar.set,
            insertbackground=CYAN,
            selectbackground=CYAN_DIM,
        )
        self.chat_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.chat_box.yview)
        self.chat_box.configure(state="disabled")

        # Text tags for styling
        self.chat_box.tag_configure("user_tag",
                                    foreground=CYAN_BRIGHT,
                                    font=("Courier New", 11, "bold"))
        self.chat_box.tag_configure("jarvis_tag",
                                    foreground=TEXT_CYAN,
                                    font=("Courier New", 11))
        self.chat_box.tag_configure("prefix_tag",
                                    foreground=AMBER,
                                    font=("Courier New", 11, "bold"))

    # =========================
    # CHAT
    # =========================
    def _chat(self, text):
        self.chat_box.configure(state="normal")

        if text.startswith("You: "):
            self.chat_box.insert(tk.END, "┌─ ", "prefix_tag")
            self.chat_box.insert(tk.END, "YOU\n", "user_tag")
            self.chat_box.insert(tk.END, "└▶ " + text[5:] + "\n\n", "user_tag")
        elif text.startswith("Jarvis: "):
            self.chat_box.insert(tk.END, "┌─ ", "prefix_tag")
            self.chat_box.insert(tk.END, "J.A.R.V.I.S.\n", "jarvis_tag")
            self.chat_box.insert(tk.END, "└▶ " + text[8:] + "\n\n", "jarvis_tag")
        else:
            self.chat_box.insert(tk.END, text + "\n")

        self.chat_box.see(tk.END)
        self.chat_box.configure(state="disabled")

    # =========================
    # STATUS
    # =========================
    def _set_status(self, status):
        self.status = status
        color_map = {
            "IDLE":      (CYAN,      TEXT_DIM,  "▶  STANDBY",    AMBER),
            "LISTENING": (CYAN,      CYAN,      "◉  LISTENING",  CYAN),
            "THINKING":  (AMBER,     AMBER,     "⟳  PROCESSING", AMBER),
            "SPEAKING":  (RED_ALERT, RED_ALERT, "▶▶ RESPONDING", RED_ALERT),
        }
        dot_c, lbl_c, mode_t, ring_c = color_map.get(
            status, (CYAN, TEXT_DIM, status, CYAN))

        self.root.after(0, lambda: self.status_dot.config(fg=dot_c))
        self.root.after(0, lambda: self.status_label.config(
            text=status, fg=lbl_c))
        self.root.after(0, lambda: self.mode_label.config(
            text=mode_t, fg=ring_c))
        self.root.after(0, lambda: self.hud_ring.set_status_color(ring_c))

    # =========================
    # PROCESS COMMAND
    # =========================
    def _process_command(self, command):
        if not command:
            return

        # ✅ SAVE USER MESSAGE
        add_chat("user", command)

        self.root.after(0, lambda: self._chat("You: " + command))
        self.root.after(0, lambda: self._set_status("THINKING"))

        def run():
            result = execute_command(command)

            if result is False:
                speak("Goodbye")
                self.running = False
                self.root.after(1000, self.root.destroy)
                return

            response = result if result else ask_ai(command)

            # ✅ SAVE ASSISTANT RESPONSE
            add_chat("assistant", response)

            self.root.after(0, lambda: self._set_status("SPEAKING"))
            self.root.after(0, lambda: self._chat("Jarvis: " + response))

            speak(response)

            self.root.after(0, lambda: self._set_status("IDLE"))

        Thread(target=run, daemon=True).start()

    # =========================
    # KEYBOARD INPUT
    # =========================
    def _send(self):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self._process_command(cmd)

    # =========================
    # VOICE LOOP (NO INTERRUPT)
    # =========================
    def _voice_loop(self):
        while self.running:
            self._set_status("LISTENING")
            command = listen()
            if command:
                self._process_command(command)
            self._set_status("IDLE")
            time.sleep(0.2)

    # =========================
    # GREETING
    # =========================
    def _greet(self):
        def greet():
            msg = "Hello, I am Jarvis. How can I help you?"
            self._chat("Jarvis: " + msg)
            speak(msg)
        self.root.after(1000, greet)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    JarvisApp()