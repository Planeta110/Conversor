import os
import platform
import subprocess
import ctypes
import sys
from rich.console import Console

def mostrar_error(msg, titulo="Error",accion=None):
    sistema = platform.system()
    respuesta = None
    console = Console()

    if sistema == "Windows":
        respuesta = ctypes.windll.user32.MessageBoxW(0, msg, titulo, 0x10)  # 1=OK

    elif sistema == "Darwin":  # macOS
        subprocess.run(["osascript", "-e", f'display alert "{titulo}" message "{msg}" as critical'])
        respuesta = True

    elif sistema == "Linux":
        try:
            subprocess.run(["zenity", "--error", "--text", msg, "--title", titulo])
            respuesta = True
        except FileNotFoundError:
            print(f"❌ {titulo}: {msg}")
            respuesta = input("Pulsa Enter para continuar...")

    else:
        print(f"❌ {titulo}: {msg}")
        respuesta = input("Pulsa Enter para continuar...")

    # Ejecutar acción si se definió
    if accion:
        console.log("❌---Error DETECTED---❌")
        accion()

# Ejemplo de uso:




#import customtkinter as ctk
#import sys
#
#def errorpage(console):
#
#    class App(ctk.CTk):
#        def __init__(self, fg_color=None, **kwargs):
#            super().__init__(fg_color, **kwargs)
#
#            self.title("Error Detected")
#            self.width = 400
#            self.height = 100
#            self.geometry(f"{self.width}x{self.height}")
#            self.minsize(self.width, self.height)
#            self.maxsize(self.width, self.height)
#            self.overrideredirect(True)
#            self._set_appearance_mode("light")
#
#            self.grab_set()  # Hace que bloquee la ventana de abajo
#            self.focus()     # Pone el foco en esta ventana
#            self.frame = MainFrame(self)
#            self.frame.pack(expand=True, fill="both")
#
#            self.center_window()
#            
#        def center_window(self):
#            screen_width = self.winfo_screenwidth()   # ancho de pantalla en píxeles
#            screen_height = self.winfo_screenheight() # alto de pantalla en píxeles
#
#            x = (screen_width - self.width) // 2
#            y = (screen_height - self.height) // 2
#
#            self.geometry(f"{self.width}x{self.height}+{x}+{y}")
#
#    class MainFrame(ctk.CTkFrame):
#        def __init__(self, master, **kwargs):
#            super().__init__(master, **kwargs)
#
#            frame = ctk.CTkFrame(self, fg_color="white")
#            frame.pack(expand=True, fill="both")
#
#            # Centrar horizontalmente todo el contenido
#            container = ctk.CTkFrame(frame, fg_color="transparent")
#            container.place(relx=0.5, rely=0.5, anchor="center")
#
#            self.label = ctk.CTkLabel(container, text="Error DETECTED", font=("Arial", 18), text_color="red")
#            self.label.grid(row=0, column=0, padx=10)
#
#            self.button = ctk.CTkButton(
#                container,
#                text="OK",
#                command=self.on_click,
#                fg_color="black",
#                hover_color="#252525",
#                text_color="white"
#            )
#            self.button.grid(row=0, column=1, padx=10)
#
#        def on_click(self):
#            console.log("-ERROR-❌ CLOSING APP ❌-ERROR-")
#            sys.exit()
#
#    app = App()
#    app.mainloop()
#
#if __name__ == "__main__":
#    errorpage()
#