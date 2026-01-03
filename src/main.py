import flet as ft
import platform
import os
import sys
import click
from rich.console import Console
from others.error.error import mostrar_error
from convert import export
import json
import io

console = Console()

# --- PARCHE PARA EL EXE ---
if sys.stdout is None: sys.stdout = io.StringIO()
if sys.stderr is None: sys.stderr = io.StringIO()
if sys.stdin is None: sys.stdin = io.StringIO() # Evita el NoneType en stdin
# ---------------------------

def main(page: ft.Page):
    page.title = "iT Converto"
    page.window.icon = os.path.join("media", "logoprueba.ico")
    page.window.width = 1200
    page.window.height = 750
    page.window.resizable = False
    page.window.minimizable = True
    page.window.maximizable = False
    page.window.title_bar_hidden = True
    page.bgcolor = "#eaeaea"
    page.theme_mode = ft.ThemeMode.LIGHT

    # -----------------------------
    # LISTA ACUMULADA
    # -----------------------------
    selected_files = []

    # -----------------------------
    # GRID DE PREVIEW
    # -----------------------------
    preview_grid = ft.GridView(
        expand=True,
        max_extent=200,
        child_aspect_ratio=1,
        spacing=10,
        run_spacing=10,
    )

    # -----------------------------
    # PLACEHOLDER (imagen inicial)
    # -----------------------------
    logo_mv = os.path.join(os.path.dirname(__file__), "media", "fondomv.png")
    empty_placeholder = ft.Container(
        content=ft.Column(
            [
                ft.Image(src=logo_mv, fit=ft.ImageFit.CONTAIN, height=300),
                ft.Text("Files go here🌏", size=20, color="black")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        alignment=ft.alignment.center
    )

    # -----------------------------
    # BORDER BOX
    # -----------------------------
    border_box = ft.Container(
        content=empty_placeholder,
        width=780,
        height=460,
        padding=10,
        bgcolor="white",
        border=ft.border.all(2, "black"),
        border_radius=10,
        alignment=ft.alignment.center
    )

    # -----------------------------
    # FILE PICKER
    # -----------------------------
    def on_file_selected(e: ft.FilePickerResultEvent):
        json_path = os.path.join(
            os.path.dirname(__file__), "suported_ext.json")
        with open(json_path, "r", encoding="utf-8") as f:
            suported_files = json.load(f)

        sp_files = suported_files["supported_extensions"]

        if e.files:
            for archivo in e.files:
                ext = archivo.name.lower()
                # Corrección ligera de lógica en la extensión
                soportado = any(ext.endswith(f".{x}") for x in sp_files) or ext.endswith(tuple(sp_files))

                if not soportado:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Archivo no soportado: {archivo.name}"),
                        bgcolor="red"
                    )
                    page.snack_bar.open = True
                    page.update()
                    continue

                if any(f.name == archivo.name for f in selected_files) and soportado:
                    continue

                # Añade archivo
                selected_files.append(archivo)

                # Preview de imagen
                preview_widget = ft.Image(
                    src=archivo.path,
                    fit=ft.ImageFit.CONTAIN,
                    height=120,
                    width=120
                )

                # Icono + nombre
                bottom_row = ft.Row(
                    [
                        ft.Image(
                            src=os.path.join(os.path.dirname(
                                __file__), "media", "imgpictograma.png"),
                            height=20,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        ft.Text(
                            archivo.name,
                            size=13,
                            color="black",
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=1
                )

                # Tarjeta completa
                preview_grid.controls.append(
                    ft.GestureDetector(
                        ft.Container(
                            content=ft.Column(
                                [
                                    preview_widget,
                                    bottom_row
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            bgcolor="#ffffff",
                            on_hover=make_hover_handler("#e5e5e5", "#ffffff"),
                            padding=10,
                            border_radius=12,
                            alignment=ft.alignment.center,
                            width=150,
                        ),
                        mouse_cursor=ft.MouseCursor.CLICK
                    )
                )

            # Cambia el contenido del border_box al preview_grid
            border_box.content = preview_grid

        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("No file selected"),
                bgcolor="red"
            )
            page.snack_bar.open = True

        border_box.update()
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    # -----------------------------
    # BARRA SUPERIOR
    # -----------------------------
    logo_path = os.path.join(os.path.dirname(
        __file__), "media", "logoprueba.png")
    custom_bar = ft.Container(
        content=ft.Row(
            [
                ft.WindowDragArea(
                    content=ft.Row(
                        [
                            ft.Image(src=logo_path, width=25, height=25),
                            ft.Text("Converto", size=20,
                                    color="black", weight="bold"),
                        ],
                        spacing=10,
                    ),
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    tooltip="Cerrar",
                    on_click=lambda e: page.window.close()
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor="white",
        padding=ft.padding.only(left=10, right=10),
        height=40,
    )

    # -----------------------------
    # EFECTOS HOVER
    # -----------------------------
    def make_hover_handler(color_hover, color_no_hover):
        def handler(e):
            e.control.bgcolor = color_hover if e.data == "true" else color_no_hover
            e.control.update()
        return handler

    convert_button = ft.Container(
        content=ft.Text("Convert", size=18, color="white"),
        width=220,
        height=50,
        bgcolor="#6cd54c",
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=lambda _: export(page, selected_files=selected_files, drop_convert=drop_convert),
        on_hover=make_hover_handler("#77da5a", "#6cd54c")
    )

    select_button = ft.Container(
        content=ft.Text("Select File", size=15, color="black"),
        width=100,
        height=32,
        bgcolor="white",
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        on_hover=make_hover_handler("#f3f3f3", "white")
    )

    # -----------------------------
    # CONTENIDO PRINCIPAL
    # -----------------------------
    json_path = os.path.join(
        os.path.dirname(__file__), "suported_ext.json")
    with open(json_path, "r", encoding="utf-8") as f:
        suported_files = json.load(f)

    sp_files = suported_files["supported_extensions"]
    lista_final = []
    for i in sp_files:
        lista_final.append(ft.dropdown.Option(i.upper()))

    drop_convert = ft.Dropdown(
        value="PNG",
        width=140,
        options=lista_final
    )

    content_column = ft.Column(
        [
            custom_bar,
            border_box,
            ft.Row([select_button], alignment="center"),
            ft.Row(
                [
                    ft.Text("Convert to", size=18, color="black"),
                    drop_convert
                ],
                alignment="center",
                spacing=5
            ),
            convert_button
        ],
        horizontal_alignment="center",
        spacing=10
    )

    page.add(ft.Container(content=content_column, alignment=ft.alignment.center))


# ======================================================
# CLI + DETECT S.O.
# ======================================================
def detect_system():
    # Usamos try/except porque console.log puede fallar en el EXE sin consola
    try:
        sistema = platform.system()
        if sistema == "Windows":
            console.log("Estás en Windows 🪟", style="magenta")
        elif sistema == "Linux":
            console.log("Estás en Linux 🐧", style="magenta")
        elif sistema == "Darwin":
            console.log("Estás en macOS 🍎", style="magenta")
        else:
            mostrar_error("We don't know your system", accion=lambda: sys.exit())
    except:
        pass

@click.command()
@click.option("--version", "-v", is_flag=True)
@click.option("--gui", is_flag=True)
@click.option("--test", is_flag=True)
def cli(version, gui, test):
    if version:
        print("Versión 1.0.0")
        sys.exit()
    if test:
        try:
            console.log("----Test MODE----", style="blue")
            console.log("Executing test")
        except:
            pass
        sys.exit()
    if gui:
        ft.app(target=main)


def main_cli():
    # Blindaje total para el isatty
    try:
        if sys.stdin and hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
            cli(standalone_mode=False)
    except:
        pass
        
    detect_system()
    ft.app(target=main)


if __name__ == "__main__":
    main_cli()