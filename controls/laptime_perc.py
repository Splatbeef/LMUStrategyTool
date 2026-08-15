import flet as ft

class LapTimePerc(ft.Container):
    def __init__(self, laptime: float, referencetime: float, width: int = 80):
        percent = (laptime / referencetime)*100
        diff = laptime - referencetime
        if diff >= 0:
            diff_text = f"+{diff:.3f}s"
        else:
            diff_text = f"{diff:.3f}s"

        super().__init__(
            width=width,
            bgcolor = self.delta_color(percent),
            border_radius=10,
            padding=5,
            content=ft.Text(
                f"{percent:.2f}%",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
                text_align=ft.TextAlign.CENTER,
                size=16
                )
        )

    def delta_color(self, percent: float) -> str:
        if percent <= 100:
            return "#7DFF7D"
        if percent >= 107:
            return "#FF7D7D"

        ratio = (percent-100)/7
        start = (125, 255, 125)
        end = (255, 125, 125)
        r = int(start[0]+ratio*(end[0]-start[0]))
        g = int(start[1]+ratio*(end[1]-start[1]))
        b = int(start[2]+ratio*(end[2]-start[2]))
        return f"#{r:02X}{g:02X}{b:02X}"