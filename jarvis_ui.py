import tkinter as tk
from threading import Thread
import math
import random
import time

# ✅ REAL IMPORTS (IMPORTANT)
from voice import listen, speak
from my_commands import execute_command
from ai_brain import ask_ai

# =========================
# COLORS
# =========================
BG_DARK      = "#070d14"
BG_PANEL     = "#050b12"
BG_CARD      = "#0a1a24"
BORDER_DIM   = "#0d2a3a"
BORDER_MID   = "#1a5c7a"
BORDER_BRIGHT= "#1a7a9a"
CYAN         = "#00d4ff"
CYAN_DIM     = "#1a7a9a"
CYAN_FAINT   = "#1a5c7a"
PURPLE       = "#8040ff"
PURPLE_DIM   = "#2a0d5a"
RED_ALERT    = "#ff4060"
GREEN_OK     = "#00ff88"
AMBER        = "#ffaa00"
TEXT_CYAN    = "#7ad4f0"
TEXT_PURPLE  = "#b88aff"


# =========================
# APP CLASS
# =========================
class JarvisApp:
    def __init__(self):
        self.running = True
        self.status  = "IDLE"
        self.start_time = time.time()
        self.angle  = 0
        self.angle2 = 0
        self.angle3 = 0
        self.wave_phase = 0
        self.pulse_r    = 32
        self.pulse_dir  = 1

        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S  ///  Neural Interface")
        self.root.geometry("960x580")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self._build_ui()
        self._start_animations()
        self._greet()

        Thread(target=self._voice_loop, daemon=True).start()
        self.root.mainloop()

    # =========================
    # UI BUILD
    # =========================
    def _build_ui(self):

        # ── LEFT PANEL ──────────────────────────────────────────
        self.left = tk.Frame(self.root, bg=BG_PANEL, width=268)
        self.left.pack(side="left", fill="y")
        self.left.pack_propagate(False)

        # Brand
        tk.Label(self.left,
                 text="J . A . R . V . I . S",
                 fg=CYAN_FAINT, bg=BG_PANEL,
                 font=("Courier New", 9, "bold")).pack(pady=(16, 2))

        tk.Label(self.left,
                 text="ADVANCED  AI  SYSTEM",
                 fg=BORDER_DIM, bg=BG_PANEL,
                 font=("Courier New", 7)).pack()

        # ── CORE CANVAS ─────────────────────────────────────────
        self.canvas = tk.Canvas(self.left, width=220, height=220,
                                bg=BG_PANEL, highlightthickness=0)
        self.canvas.pack(pady=10)
        self._draw_core()

        # ── STATUS ROW ──────────────────────────────────────────
        srow = tk.Frame(self.left, bg=BG_PANEL)
        srow.pack(pady=(2, 6))

        self._dot_cv = tk.Canvas(srow, width=10, height=10,
                                 bg=BG_PANEL, highlightthickness=0)
        self._dot_cv.pack(side="left", padx=(0, 6))
        self._dot = self._dot_cv.create_oval(1, 1, 9, 9, fill=CYAN, outline="")

        self.status_label = tk.Label(srow, text="IDLE",
                                     fg=CYAN_DIM, bg=BG_PANEL,
                                     font=("Courier New", 10, "bold"), width=10, anchor="w")
        self.status_label.pack(side="left")

        # ── METRIC CARDS ────────────────────────────────────────
        mgrid = tk.Frame(self.left, bg=BG_PANEL)
        mgrid.pack(padx=14, pady=4, fill="x")

        self._cpu = tk.StringVar(value="---%")
        self._mem = tk.StringVar(value="-.--G")
        self._net = tk.StringVar(value="↑↓")
        self._upt = tk.StringVar(value="00:00")

        for i, (lbl, var) in enumerate([("CPU", self._cpu), ("MEM", self._mem),
                                         ("NET", self._net), ("UPTIME", self._upt)]):
            r, c = divmod(i, 2)
            card = tk.Frame(mgrid, bg=BG_CARD,
                            highlightbackground=BORDER_DIM, highlightthickness=1)
            card.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            mgrid.columnconfigure(c, weight=1)
            tk.Label(card, text=lbl, fg=CYAN_FAINT, bg=BG_CARD,
                     font=("Courier New", 8)).pack(pady=(6, 0))
            tk.Label(card, textvariable=var, fg=CYAN, bg=BG_CARD,
                     font=("Courier New", 12, "bold")).pack(pady=(0, 6))

        # ── WAVEFORM ────────────────────────────────────────────
        tk.Label(self.left, text="AUDIO INPUT", fg=CYAN_FAINT, bg=BG_PANEL,
                 font=("Courier New", 8)).pack(anchor="w", padx=16, pady=(8, 2))

        self._wave_cv = tk.Canvas(self.left, width=236, height=42,
                                  bg=BG_CARD,
                                  highlightbackground=BORDER_DIM,
                                  highlightthickness=1)
        self._wave_cv.pack(padx=16)
        self._wave_ln = self._wave_cv.create_line(0, 21, 236, 21,
                                                   fill=CYAN_FAINT, width=1.5,
                                                   smooth=True)

        # ── RIGHT PANEL ─────────────────────────────────────────
        self.right = tk.Frame(self.root, bg=BG_DARK)
        self.right.pack(side="right", fill="both", expand=True)

        # Header bar
        hdr = tk.Frame(self.right, bg=BG_PANEL,
                       highlightbackground=BORDER_DIM, highlightthickness=1,
                       height=34)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="NEURAL INTERFACE  ///  ACTIVE SESSION",
                 fg=BORDER_BRIGHT, bg=BG_PANEL,
                 font=("Courier New", 9)).pack(side="left", padx=14)

        drow = tk.Frame(hdr, bg=BG_PANEL)
        drow.pack(side="right", padx=12)
        for col in [RED_ALERT, AMBER, CYAN]:
            dc = tk.Canvas(drow, width=10, height=10, bg=BG_PANEL, highlightthickness=0)
            dc.pack(side="left", padx=3, pady=12)
            dc.create_oval(1, 1, 9, 9, fill=col, outline="")

        # Chat area + scrollbar
        chat_wrap = tk.Frame(self.right, bg=BG_DARK)
        chat_wrap.pack(fill="both", expand=True)

        sb = tk.Scrollbar(chat_wrap, bg=BG_PANEL, troughcolor=BG_DARK,
                          activebackground=CYAN_DIM, width=6, relief="flat")
        sb.pack(side="right", fill="y")

        self.chat_box = tk.Text(
            chat_wrap,
            bg=BG_DARK, fg=TEXT_CYAN,
            font=("Courier New", 12),
            wrap="word", padx=14, pady=12,
            relief="flat", cursor="arrow",
            insertbackground=CYAN,
            selectbackground=BORDER_DIM,
            yscrollcommand=sb.set,
        )
        self.chat_box.pack(side="left", fill="both", expand=True)
        sb.config(command=self.chat_box.yview)

        # Color tags
        self.chat_box.tag_config("sys_pre",   foreground=CYAN_FAINT)
        self.chat_box.tag_config("jarvis",    foreground=TEXT_CYAN)
        self.chat_box.tag_config("usr_pre",   foreground="#5a2a9a")
        self.chat_box.tag_config("user",      foreground=TEXT_PURPLE)
        self.chat_box.tag_config("boot",      foreground=BORDER_DIM)
        self.chat_box.tag_config("boot_ok",   foreground=GREEN_OK)
        self.chat_box.tag_config("divider",   foreground=BORDER_DIM)
        self.chat_box.configure(state="disabled")

        # Boot text
        self._boot()

        # ── INPUT BAR ───────────────────────────────────────────
        ibar = tk.Frame(self.right, bg=BG_PANEL,
                        highlightbackground=BORDER_DIM, highlightthickness=1,
                        height=50)
        ibar.pack(fill="x")
        ibar.pack_propagate(False)

        tk.Label(ibar, text=" >", fg=CYAN, bg=BG_PANEL,
                 font=("Courier New", 14, "bold")).pack(side="left", padx=(10, 2))

        self.entry = tk.Entry(
            ibar,
            bg=BG_PANEL, fg=CYAN,
            insertbackground=CYAN,
            relief="flat",
            font=("Courier New", 13),
            selectbackground=BORDER_DIM,
        )
        self.entry.pack(side="left", fill="both", expand=True, pady=10)
        self.entry.bind("<Return>", lambda e: self._send())

        # Send button
        send = tk.Canvas(ibar, width=36, height=36, bg=BG_CARD,
                         highlightbackground=BORDER_MID, highlightthickness=1,
                         cursor="hand2")
        send.pack(side="right", padx=10, pady=7)
        send.create_text(18, 18, text="▶", fill=CYAN, font=("Courier New", 12, "bold"))
        send.bind("<Button-1>", lambda e: self._send())

    # =========================
    # CORE DRAWING
    # =========================
    def _draw_core(self):
        cx, cy = 110, 110

        # Static rings
        self.canvas.create_oval(8,  8,  212, 212, outline=BORDER_DIM,  width=1)
        self.canvas.create_oval(32, 32, 188, 188, outline=BORDER_DIM,  width=1)
        self.canvas.create_oval(58, 58, 162, 162, outline=BORDER_DIM,  width=1)

        # Tick marks
        for deg in [0, 90, 180, 270]:
            r = math.radians(deg)
            self.canvas.create_line(
                cx + 101*math.cos(r), cy + 101*math.sin(r),
                cx + 90 *math.cos(r), cy + 90 *math.sin(r),
                fill=BORDER_MID, width=1.5)

        # Inner core face
        self.canvas.create_oval(78, 78, 142, 142, fill=BG_CARD, outline=CYAN_FAINT, width=1)
        self.canvas.create_text(cx, cy - 8, text="J.A.R.V.I.S",
                                fill=CYAN_FAINT, font=("Courier New", 8, "bold"))
        self._core_txt = self.canvas.create_text(cx, cy + 8, text="ONLINE",
                                                  fill=CYAN, font=("Courier New", 8, "bold"))

        # Animated arcs
        self.arc1 = self.canvas.create_arc(8,  8,  212, 212, start=0, extent=55,
                                            outline=CYAN,      width=2.5, style="arc")
        self.arc2 = self.canvas.create_arc(32, 32, 188, 188, start=0, extent=80,
                                            outline="#00bcd4", width=2,   style="arc")
        self.arc3 = self.canvas.create_arc(58, 58, 162, 162, start=0, extent=40,
                                            outline=CYAN_DIM,  width=1.5, style="arc")

        # Orbit dot
        self._orb = self.canvas.create_oval(0, 0, 8, 8, fill=CYAN, outline="")

        # Pulse ring
        self._pulse = self.canvas.create_oval(
            cx-32, cy-32, cx+32, cy+32, outline=CYAN, width=0.5)

    # =========================
    # ANIMATIONS
    # =========================
    def _start_animations(self):
        self._animate_core()
        self._animate_wave()
        self._update_metrics()

    def _animate_core(self):
        cx, cy = 110, 110

        self.angle  = (self.angle  + 3) % 360
        self.angle2 = (self.angle2 - 5) % 360
        self.angle3 = (self.angle3 + 7) % 360

        self.canvas.itemconfig(self.arc1, start=self.angle)
        self.canvas.itemconfig(self.arc2, start=self.angle2)
        self.canvas.itemconfig(self.arc3, start=self.angle3)

        # Orbit dot
        rad = math.radians(self.angle)
        ox = cx + 101 * math.cos(rad) - 4
        oy = cy + 101 * math.sin(rad) - 4
        self.canvas.coords(self._orb, ox, oy, ox+8, oy+8)

        # Pulse ring
        self.pulse_r += 0.2 * self.pulse_dir
        if self.pulse_r > 37 or self.pulse_r < 30:
            self.pulse_dir *= -1
        pr = self.pulse_r
        self.canvas.coords(self._pulse, cx-pr, cy-pr, cx+pr, cy+pr)

        # Color by status
        col = RED_ALERT if self.status == "SPEAKING"  else \
              GREEN_OK  if self.status == "LISTENING" else \
              AMBER     if self.status == "THINKING"  else CYAN
        self.canvas.itemconfig(self.arc1,   outline=col)
        self.canvas.itemconfig(self._pulse, outline=col)
        self.canvas.itemconfig(self._orb,   fill=col)

        self.root.after(40, self._animate_core)

    def _animate_wave(self):
        self.wave_phase += 0.10
        pts = []
        for x in range(0, 237, 4):
            amp = 14 if self.status == "SPEAKING"  else \
                   8 if self.status == "LISTENING" else 2
            y = 21 + math.sin(x * 0.08 + self.wave_phase) * amp * \
                     math.sin(x * 0.025 + self.wave_phase * 0.4)
            pts.extend([x, y])
        if len(pts) >= 4:
            self._wave_cv.coords(self._wave_ln, *pts)
            col = RED_ALERT if self.status == "SPEAKING"  else \
                  GREEN_OK  if self.status == "LISTENING" else CYAN_FAINT
            self._wave_cv.itemconfig(self._wave_ln, fill=col)
        self.root.after(40, self._animate_wave)

    def _update_metrics(self):
        elapsed = int(time.time() - self.start_time)
        self._upt.set(f"{elapsed//60:02d}:{elapsed%60:02d}")
        self._cpu.set(f"{random.randint(8, 28)}%")
        self._mem.set(f"{random.uniform(3.8, 5.2):.1f}G")
        self._net.set(random.choice(["↑↓", "↑ ", " ↓"]))
        self.root.after(1000, self._update_metrics)

    # =========================
    # STATUS
    # =========================
    def _set_status(self, status):
        self.status = status
        colors = {"IDLE": CYAN, "SPEAKING": RED_ALERT,
                  "LISTENING": GREEN_OK, "THINKING": AMBER}
        col = colors.get(status, CYAN)
        self.status_label.config(text=status, fg=col)
        self._dot_cv.itemconfig(self._dot, fill=col)
        self.canvas.itemconfig(self._core_txt, text=status, fill=col)

    # =========================
    # CHAT
    # =========================
    def _boot(self):
        self.chat_box.configure(state="normal")
        for tag, txt in [
            ("boot",    "> SYSTEM BOOT v3.14.159\n"),
            ("boot",    "> Neural core..........."), ("boot_ok", "OK\n"),
            ("boot",    "> Voice synthesis......."), ("boot_ok", "OK\n"),
            ("boot",    "> AI subsystems........."), ("boot_ok", "ONLINE\n"),
            ("divider", "─" * 50 + "\n"),
        ]:
            self.chat_box.insert(tk.END, txt, tag)
        self.chat_box.configure(state="disabled")

    def _chat(self, text):
        """Drop-in replacement — keeps same call signature as original."""
        self.chat_box.configure(state="normal")
        ts = time.strftime("%H.%M.%S")

        if text.startswith("You: "):
            msg = text[5:]
            self.chat_box.insert(tk.END, f"[{ts}] ", "divider")
            self.chat_box.insert(tk.END, "YOU    ▸ ", "usr_pre")
            self.chat_box.insert(tk.END, msg + "\n", "user")
        elif text.startswith("Jarvis: "):
            msg = text[8:]
            self.chat_box.insert(tk.END, f"[{ts}] ", "divider")
            self.chat_box.insert(tk.END, "JARVIS ▸ ", "sys_pre")
            self.chat_box.insert(tk.END, msg + "\n", "jarvis")
        else:
            self.chat_box.insert(tk.END, text + "\n", "jarvis")

        self.chat_box.see(tk.END)
        self.chat_box.configure(state="disabled")

    # =========================
    # COMMAND (unchanged logic)
    # =========================
    def _process_command(self, command):
        if not command:
            return

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

            self.root.after(0, lambda: self._set_status("SPEAKING"))
            self.root.after(0, lambda: self._chat("Jarvis: " + response))

            speak(response)

            self.root.after(0, lambda: self._set_status("IDLE"))

        Thread(target=run, daemon=True).start()

    def _send(self):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self._process_command(cmd)

    # =========================
    # VOICE LOOP (unchanged)
    # =========================
    def _voice_loop(self):
        while self.running:
            self.root.after(0, lambda: self._set_status("LISTENING"))
            command = listen()
            if command:
                self._process_command(command)
            self.root.after(0, lambda: self._set_status("IDLE"))
            time.sleep(0.1)

    # =========================
    # GREETING (unchanged)
    # =========================
    def _greet(self):
        def greet():
            msg = "Hello, I am Jarvis. How can I help you?"
            self._chat("Jarvis: " + msg)
            self._set_status("SPEAKING")
            speak(msg)
            self._set_status("IDLE")
        self.root.after(1000, greet)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    JarvisApp()