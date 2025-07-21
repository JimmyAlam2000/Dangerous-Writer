import tkinter as tk
from tkinter import messagebox, filedialog
import time

# === SETTINGS ===
INACTIVITY_LIMIT = 5         # seconds of inactivity allowed
SESSION_DURATION = 180       # total time user must keep typing (in seconds)

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚠️ Dangerous Writing App (Enhanced)")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.start_time = time.time()
        self.last_typed_time = time.time()
        self.session_active = True

        # === UI Elements ===
        self.timer_label = tk.Label(
            root, text="", font=("Helvetica", 16), fg="white", bg="#1e1e1e"
        )
        self.timer_label.pack(pady=10)

        self.text_box = tk.Text(
            root,
            font=("Courier", 14),
            wrap=tk.WORD,
            bg="#2e2e2e",
            fg="white",
            insertbackground="white",
            undo=True,
        )
        self.text_box.pack(expand=True, fill="both", padx=20, pady=10)
        self.text_box.bind("<Key>", self.reset_timer)

        self.save_button = tk.Button(
            root,
            text="💾 Save Work",
            state="disabled",
            command=self.save_text,
            bg="#444",
            fg="white"
        )
        self.save_button.pack(pady=10)

        self.word_count_label = tk.Label(
            root, text="Words: 0", font=("Helvetica", 12), fg="gray", bg="#1e1e1e"
        )
        self.word_count_label.pack(pady=5)

        self.update_timer()

    def reset_timer(self, event=None):
        if self.session_active:
            self.last_typed_time = time.time()
            self.text_box.configure(bg="#2e2e2e")
            self.update_word_count()

    def update_timer(self):
        if not self.session_active:
            return

        now = time.time()
        inactive_time = now - self.last_typed_time
        time_left = INACTIVITY_LIMIT - inactive_time
        session_remaining = SESSION_DURATION - int(now - self.start_time)

        # Update countdown
        self.timer_label.config(
            text=f"⏳ Inactivity: {max(0, int(time_left))}s  |  ⌛ Time Left: {max(0, session_remaining)}s"
        )

        # Flash warning color
        if 0 < time_left <= 2:
            self.text_box.configure(bg="#802020")  # Warning red

        # Delete content if inactive
        if time_left <= 0:
            self.text_box.delete("1.0", tk.END)
            self.last_typed_time = time.time()
            self.text_box.configure(bg="#2e2e2e")
            messagebox.showwarning("Too Slow!", "You stopped typing. Everything was deleted!")

        # End session if time completed
        if session_remaining <= 0:
            self.session_active = False
            self.save_button.config(state="normal")
            self.timer_label.config(text="🎉 You survived! You can now save your writing.")
            messagebox.showinfo("Well done!", "You completed the session!")
            return

        self.root.after(1000, self.update_timer)

    def update_word_count(self):
        text = self.text_box.get("1.0", tk.END)
        words = text.strip().split()
        self.word_count_label.config(text=f"Words: {len(words)}")

    def save_text(self):
        content = self.text_box.get("1.0", tk.END).strip()
        if content:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Text files", "*.txt")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Saved", "Your work has been saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()
