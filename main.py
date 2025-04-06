import customtkinter
from MainWindow import MainWindow
from welcome import OpenLabelApp

# Initial customTkinter window setup

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        import tkinter as tk 

        if tk._default_root is None:
            tk._default_root = self

        self.geometry("700x800")
        self.title("OpenLabel")

def mainTest():
    app = App()
    app.withdraw()



    welcome = OpenLabelApp(app)
    app.wait_window(welcome)  # Wait for the welcome window to close before showing the main window

    """
    mainWindow = MainWindow(app)
    app.wait_window(mainWindow)  # Wait for the main window to close before showing the welcome window


    app.deiconify()

    app.mainloop()
    
    """
    app.deiconify()

    main_window = MainWindow(app)
    main_window.deiconify()

    app.mainloop()

if __name__ == '__main__':
    mainTest()
