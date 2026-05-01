import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, ttk, scrolledtext, messagebox
import threading
import os

from app.runner import run_localdex
from app.history import add_chat, clear_history, format_history
from app.config import PROJECT_DIR
from app.theme import *


class LocalDexWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("LocalDex")
        self.root.geometry("1250x720")
        self.root.configure(bg=BG)

        self.selected_file = None

        self.build_layout()
        self.populate_files()

        self.add_bot_message("Halo bro 👋\nKlik file di kiri buat preview/edit. Setelah edit, klik Save File.")

    def build_layout(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(main, bg=SIDEBAR_BG, width=260)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="LocalDex", font=FONT_TITLE, fg=FG, bg=SIDEBAR_BG).pack(
            anchor="w", padx=16, pady=(16, 6)
        )

        self.sidebar_btn(sidebar, "New Chat", self.clear_chat)
        self.sidebar_btn(sidebar, "Show History", self.show_history)
        self.sidebar_btn(sidebar, "Clear History", self.clear_history_ui)
        self.sidebar_btn(sidebar, "Refresh Files", self.populate_files)

        tk.Label(sidebar, text="Files", font=FONT_SUB, fg=SECONDARY, bg=SIDEBAR_BG).pack(
            anchor="w", padx=16, pady=(10, 4)
        )

        self.tree = ttk.Treeview(sidebar)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)

        center = tk.Frame(main, bg=BG)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = Canvas(center, bg=CHAT_BG, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(center, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_frame = Frame(self.canvas, bg=CHAT_BG)
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        preview_panel = tk.Frame(main, bg=SIDEBAR_BG, width=380)
        preview_panel.pack(side=tk.RIGHT, fill=tk.Y)
        preview_panel.pack_propagate(False)

        tk.Label(
            preview_panel,
            text="File Editor",
            font=FONT_TITLE,
            fg=FG,
            bg=SIDEBAR_BG
        ).pack(anchor="w", padx=14, pady=(16, 4))

        self.file_label = tk.Label(
            preview_panel,
            text="Belum ada file dipilih",
            font=FONT_SUB,
            fg=SECONDARY,
            bg=SIDEBAR_BG,
            wraplength=340,
            justify="left"
        )
        self.file_label.pack(anchor="w", padx=14, pady=(0, 10))

        self.preview_box = scrolledtext.ScrolledText(
            preview_panel,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=CHAT_BG,
            fg=FG,
            insertbackground=FG,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.preview_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))

        btn_frame = tk.Frame(preview_panel, bg=SIDEBAR_BG)
        btn_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        tk.Button(
            btn_frame,
            text="Save File",
            font=FONT_MAIN,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.FLAT,
            command=self.save_selected_file
        ).pack(fill=tk.X, ipady=7, pady=(0, 8))

        tk.Button(
            btn_frame,
            text="Explain File",
            font=FONT_MAIN,
            bg=PANEL_BG,
            fg=FG,
            relief=tk.FLAT,
            command=self.explain_selected_file
        ).pack(fill=tk.X, ipady=7, pady=(0, 8))

        tk.Button(
            btn_frame,
            text="Read in Chat",
            font=FONT_MAIN,
            bg=PANEL_BG,
            fg=FG,
            relief=tk.FLAT,
            command=self.read_selected_file
        ).pack(fill=tk.X, ipady=7)

        input_frame = tk.Frame(self.root, bg=BG)
        input_frame.pack(fill=tk.X, padx=20, pady=15)

        self.input_box = tk.Entry(
            input_frame,
            font=FONT_MAIN,
            bg=INPUT_BG,
            fg=FG,
            insertbackground=FG,
            relief=tk.FLAT
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
        self.input_box.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(
            input_frame,
            text="➜",
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.FLAT,
            command=self.send_message
        )
        self.send_btn.pack(side=tk.RIGHT, ipadx=10, ipady=8)

    def sidebar_btn(self, parent, text, cmd):
        tk.Button(
            parent,
            text=text,
            font=FONT_MAIN,
            bg=PANEL_BG,
            fg=FG,
            relief=tk.FLAT,
            anchor="w",
            command=cmd
        ).pack(fill=tk.X, padx=12, pady=4, ipady=8)

    def populate_files(self):
        self.tree.delete(*self.tree.get_children())
        self.insert_node("", PROJECT_DIR)

    def insert_node(self, parent, path):
        name = os.path.basename(path)

        if name in ["node_modules", ".git", "__pycache__", ".venv", "venv"]:
            return

        node = self.tree.insert(parent, "end", text=name, values=[str(path)])

        if os.path.isdir(path):
            try:
                for item in os.listdir(path):
                    self.insert_node(node, os.path.join(path, item))
            except Exception:
                pass

    def on_file_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if not values:
            return

        file_path = values[0]

        if os.path.isfile(file_path):
            self.selected_file = file_path
            self.preview_file(file_path)

    def preview_file(self, file_path):
        relative = os.path.relpath(file_path, PROJECT_DIR)
        self.file_label.config(text=relative)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            content = "File ini bukan text biasa atau encoding-nya tidak kebaca."
        except Exception as e:
            content = f"Error baca file: {e}"

        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, content)

    def save_selected_file(self):
        if not self.selected_file:
            messagebox.showwarning("LocalDex", "Pilih file dulu bro.")
            return

        try:
            content = self.preview_box.get("1.0", tk.END).rstrip("\n")

            with open(self.selected_file, "w", encoding="utf-8") as f:
                f.write(content)

            relative = os.path.relpath(self.selected_file, PROJECT_DIR)
            self.add_bot_message(f"File berhasil disimpan: {relative}")

        except Exception as e:
            messagebox.showerror("LocalDex", f"Gagal save file:\n{e}")

    def explain_selected_file(self):
        if not self.selected_file:
            self.add_bot_message("Pilih file dulu bro.")
            return

        relative = os.path.relpath(self.selected_file, PROJECT_DIR)
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, f"baca {relative} terus jelasin singkat")
        self.send_message()

    def read_selected_file(self):
        if not self.selected_file:
            self.add_bot_message("Pilih file dulu bro.")
            return

        relative = os.path.relpath(self.selected_file, PROJECT_DIR)
        self.input_box.delete(0, tk.END)
        self.input_box.insert(0, f"baca {relative}")
        self.send_message()

    def create_copyable_bubble(self, parent, text, is_user=False):
        bubble = tk.Text(
            parent,
            wrap="word",
            font=FONT_MAIN,
            bg=USER_BG if is_user else BOT_BG,
            fg=FG,
            insertbackground=FG,
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=8,
            width=70,
            height=max(1, min(text.count("\n") + 1, 12))
        )

        bubble.insert("1.0", text)
        bubble.configure(state=tk.DISABLED)
        return bubble

    def add_user_message(self, text):
        frame = tk.Frame(self.chat_frame, bg=CHAT_BG)
        frame.pack(fill=tk.X, pady=5, padx=10)

        bubble = self.create_copyable_bubble(frame, text, is_user=True)
        bubble.pack(anchor="e")

        self.scroll_down()

    def add_bot_message(self, text):
        frame = tk.Frame(self.chat_frame, bg=CHAT_BG)
        frame.pack(fill=tk.X, pady=5, padx=10)

        bubble = self.create_copyable_bubble(frame, text, is_user=False)
        bubble.pack(anchor="w")

        self.scroll_down()

    def stream_bot_message(self, text, bubble=None, index=0):
        if bubble is None:
            frame = tk.Frame(self.chat_frame, bg=CHAT_BG)
            frame.pack(fill=tk.X, pady=5, padx=10)

            bubble = self.create_copyable_bubble(frame, "", is_user=False)
            bubble.pack(anchor="w")

        if index < len(text):
            bubble.configure(state=tk.NORMAL)
            bubble.insert(tk.END, text[index])
            bubble.configure(state=tk.DISABLED)
            self.root.after(5, lambda: self.stream_bot_message(text, bubble, index + 1))
        else:
            add_chat("assistant", text)
            self.finish_ui()

        self.scroll_down()

    def scroll_down(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def send_message(self, event=None):
        prompt = self.input_box.get().strip()
        if not prompt:
            return

        self.input_box.delete(0, tk.END)
        self.add_user_message(prompt)
        add_chat("user", prompt)

        self.send_btn.config(state=tk.DISABLED)
        self.input_box.config(state=tk.DISABLED)

        threading.Thread(target=self.process, args=(prompt,), daemon=True).start()

    def process(self, prompt):
        result = run_localdex(prompt)
        self.root.after(0, lambda: self.stream_bot_message(result))

    def finish_ui(self):
        self.send_btn.config(state=tk.NORMAL)
        self.input_box.config(state=tk.NORMAL)
        self.input_box.focus()

    def clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.add_bot_message("Chat baru siap bro.")

    def show_history(self):
        self.add_bot_message(format_history())

    def clear_history_ui(self):
        clear_history()
        self.add_bot_message("History dihapus.")