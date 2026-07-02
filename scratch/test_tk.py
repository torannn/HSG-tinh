try:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print("Tkinter initialized successfully!")
    root.destroy()
except Exception as e:
    print("Tkinter initialization failed!")
    print("Error:", e)
    import traceback
    traceback.print_exc()
