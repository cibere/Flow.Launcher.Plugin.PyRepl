import tkinter as tk


class ErrorWindow(tk.Tk):
    def __init__(self, title: str, detail: str):
        super().__init__()
        self.title(title)
        self.geometry("500x200")
        self.iconphoto(False, tk.PhotoImage(file="icon.png"))
        self.minsize(350, 75)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.lift()

        text_frame = tk.Frame(self)
        text_frame.grid(row=1, column=0, padx=(7, 7), pady=(7, 7), sticky="nsew")
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        self.textbox = tk.Text(text_frame, height=6)
        self.textbox.insert("1.0", detail)
        self.textbox.grid(row=0, column=0, sticky="nsew")


def show_error(title: str, msg: str):
    ErrorWindow(title, msg).mainloop()

if __name__ == "__main__":
    import sys
    show_error("PyRepl Error", " ".join(sys.argv))