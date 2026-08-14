import flet as ft

def delta_color(percent: float) -> str:
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

print(delta_color(103))
