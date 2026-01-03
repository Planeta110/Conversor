import threading
import os
import winsound  # Sonido del sistema
from PIL import Image
import flet as ft

def export(page: ft.Page, selected_files, drop_convert):
    if not selected_files:
        page.snack_bar = ft.SnackBar(ft.Text("No hay archivos seleccionados"), bgcolor="red")
        page.snack_bar.open = True
        page.update()
        return

    home = os.path.expanduser("~")
    downloads = os.path.join(home, "Downloads")
    target_ext = drop_convert.value.lower()
    
    # Contador para saber cuándo terminan todos
    finalizados_count = [0] 
    total_archivos = len(selected_files)

    def close_overlay(e):
        page.overlay.remove(overlay_wrapper)
        page.update()

    # Título dinámico para cambiar a "Finalizado"
    titulo_texto = ft.Text("Procesando...", size=18, color="#1e293b", weight="bold")
    
    overlay_column = ft.Column(
        [ft.Row([
            titulo_texto,
            ft.IconButton(
                icon=ft.Icons.CLOSE_ROUNDED,
                icon_color="#64748b",
                on_click=close_overlay
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)],
        spacing=15,
        scroll=ft.ScrollMode.AUTO
    )

    progreso_containers = []

    for foto in selected_files:
        barra_row = ft.Row(
            [
                # El texto se queda en Gris/Negro (Slate 600) como pediste
                ft.Text(f"{foto.name}", size=13, color="#475569", width=140, no_wrap=True),
                ft.ProgressBar(width=280, height=6, bgcolor="#e2e8f0", color="#334155", value=0),
                ft.Icon(name=None, size=18) # Espacio para el check chulo
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        overlay_column.controls.append(barra_row)
        progreso_containers.append({
            "bar": barra_row.controls[1],
            "icon": barra_row.controls[2]
        })

    overlay_container = ft.Container(
        content=overlay_column,
        width=520,
        height=min(100 + len(selected_files)*45, 450),
        bgcolor="#f8fafc", 
        padding=25,
        border_radius=20,
        border=ft.border.all(1, "#e2e8f0"),
        shadow=ft.BoxShadow(blur_radius=30, color="#0000001A", offset=ft.Offset(0, 15))
    )

    overlay_wrapper = ft.Container(
        content=overlay_container,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#00000033"
    )

    page.overlay.append(overlay_wrapper)
    page.update()

    def transformar(i, foto):
        try:
            with Image.open(foto.path) as img:
                nombre_sin_ext = os.path.splitext(foto.name)[0]
                formato = "JPEG" if target_ext in ("jpg", "jpeg") else target_ext.upper()
                ruta_completa = os.path.join(downloads, f"{nombre_sin_ext}.{target_ext}")
                img.save(ruta_completa, formato)
            
            progreso_containers[i]["bar"].value = 1.0
            progreso_containers[i]["icon"].name = ft.Icons.CHECK_CIRCLE_ROUNDED
            progreso_containers[i]["icon"].color = "#10b981"
            
        except Exception:
            progreso_containers[i]["icon"].name = ft.Icons.ERROR_OUTLINE_ROUNDED
            progreso_containers[i]["icon"].color = "#ef4444"
        
        finally:
            finalizados_count[0] += 1
            # Si todos han terminado
            if finalizados_count[0] == total_archivos:
                titulo_texto.value = "Finalizado ✅"
                titulo_texto.color = "#0f172a"
                page.update()
                # Sonido de Windows (Asterisk es el de notificación)
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                page.update()

    for i, foto in enumerate(selected_files):
        threading.Thread(target=transformar, args=(i, foto), daemon=True).start()