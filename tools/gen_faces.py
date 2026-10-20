#!/usr/bin/env python3
"""Gera as 20 faces (color + bump map) do d20 "Orelha-de-Prata" para o Dice So Nice.

Saida:
  assets/faces/d20_01.png ... d20_20.png        (cor, fundo transparente)
  assets/faces/d20_01_bump.png ... _bump.png    (relevo: branco = alto)
  assets/preview.png                            (folha de contato para conferir)

Parametros de ajuste (se a face ficar grande/pequena no Foundry):
  CY    : centro vertical do conteudo (0.0 topo, 1.0 base)
  RING  : raio externo da engrenagem, em fracao do lado da textura
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
FACES = os.path.join(OUT, "faces")
os.makedirs(FACES, exist_ok=True)

FINAL = 256           # tamanho final do PNG
SS = 2                # supersampling para suavizar
S = FINAL * SS
CX = S * 0.5
CY = S * 0.575
RING = S * 0.315       # raio externo da engrenagem

GOLD = (201, 162, 75, 255)
DARK = (27, 31, 38, 255)
WHITE = (255, 255, 255, 255)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


class Pen:
    """Desenha em dois modos: cor (dourado com contorno escuro) e bump (branco)."""

    def __init__(self, mode):
        self.mode = mode
        if mode == "color":
            self.img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        else:
            self.img = Image.new("RGBA", (S, S), (0, 0, 0, 255))
        self.d = ImageDraw.Draw(self.img)

    # espessuras em pixels do canvas supersampled
    def line(self, pts, w, closed=False):
        if closed:
            pts = list(pts) + [pts[0]]
        if self.mode == "color":
            self.d.line(pts, fill=DARK, width=int(w + 7 * SS), joint="curve")
            self.d.line(pts, fill=GOLD, width=int(w), joint="curve")
        else:
            self.d.line(pts, fill=WHITE, width=int(w), joint="curve")

    def ellipse(self, box, w=0, filled=False):
        x0, y0, x1, y1 = box
        if self.mode == "color":
            pad = 3.5 * SS
            self.d.ellipse((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=DARK)
            self.d.ellipse(box, fill=GOLD if filled else (0, 0, 0, 0))
            if not filled:
                # remove o miolo escuro e redesenha so o anel dourado
                inner = (x0 + w, y0 + w, x1 - w, y1 - w)
                self.d.ellipse(inner, fill=(0, 0, 0, 0))
                self.d.arc(box, 0, 360, fill=GOLD, width=int(w))
        else:
            if filled:
                self.d.ellipse(box, fill=WHITE)
            else:
                self.d.arc(box, 0, 360, fill=WHITE, width=int(w))

    def text(self, xy, txt, size):
        font = ImageFont.truetype(FONT_PATH, int(size))
        if self.mode == "color":
            self.d.text(xy, txt, font=font, fill=GOLD, anchor="mm",
                        stroke_width=int(3.5 * SS), stroke_fill=DARK)
        else:
            self.d.text(xy, txt, font=font, fill=WHITE, anchor="mm")


def gear_points(cx, cy, r_out, r_in, teeth=14):
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step
        for frac, r in ((0.0, r_in), (0.18, r_out), (0.50, r_out), (0.68, r_in)):
            ang = a + frac * step
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# ---------- simbolos (pequenos, desenhados abaixo do numero) ----------
def sym_broken_string(p, cx, cy, u):
    """1: corda partida."""
    p.line([(cx - 0.25 * u, cy - 1.4 * u), (cx - 0.25 * u, cy - 0.2 * u)], 0.34 * u)
    p.line([(cx + 0.25 * u, cy + 0.35 * u), (cx + 0.25 * u, cy + 1.4 * u)], 0.34 * u)
    # ponta enrolada da corda partida
    p.line([(cx - 0.25 * u, cy - 0.2 * u), (cx + 0.2 * u, cy + 0.05 * u),
            (cx + 0.7 * u, cy - 0.25 * u), (cx + 0.9 * u, cy - 0.7 * u)], 0.28 * u)


def sym_note(p, cx, cy, u):
    """5: nota musical."""
    p.ellipse((cx - 0.9 * u, cy + 0.25 * u, cx - 0.05 * u, cy + 0.95 * u), filled=True)
    p.line([(cx - 0.12 * u, cy + 0.6 * u), (cx - 0.12 * u, cy - 1.0 * u)], 0.2 * u)
    p.line([(cx - 0.12 * u, cy - 1.0 * u), (cx + 0.7 * u, cy - 0.5 * u),
            (cx + 0.5 * u, cy + 0.1 * u)], 0.2 * u)


def sym_clock(p, cx, cy, u):
    """10: relogio."""
    p.ellipse((cx - u, cy - u, cx + u, cy + u), w=0.2 * u)
    p.line([(cx, cy), (cx, cy - 0.65 * u)], 0.18 * u)
    p.line([(cx, cy), (cx + 0.45 * u, cy + 0.15 * u)], 0.18 * u)


def sym_gear(p, cx, cy, u):
    """15: engrenagem."""
    p.line(gear_points(cx, cy, u, 0.7 * u, teeth=8), 0.17 * u, closed=True)
    p.ellipse((cx - 0.28 * u, cy - 0.28 * u, cx + 0.28 * u, cy + 0.28 * u), filled=True)


def sym_lute(p, cx, cy, u):
    """20: alaude."""
    p.line([(cx, cy - 1.0 * u), (cx, cy - 2.2 * u)], 0.42 * u)           # braco
    p.line([(cx - 0.5 * u, cy - 2.2 * u), (cx + 0.5 * u, cy - 2.35 * u)], 0.34 * u)  # cabeca
    p.ellipse((cx - 1.0 * u, cy - 1.2 * u, cx + 1.0 * u, cy + 1.2 * u), w=0.34 * u)  # corpo
    p.ellipse((cx - 0.3 * u, cy - 0.3 * u, cx + 0.3 * u, cy + 0.3 * u), filled=True)  # boca


SYMBOLS = {1: sym_broken_string, 5: sym_note, 10: sym_clock,
           15: sym_gear, 20: sym_lute}


SYM_LAYOUT = {1: (0.26, 0.47), 5: (0.27, 0.50), 10: (0.27, 0.50),
              15: (0.27, 0.50), 20: (0.25, 0.50)}


def render(n, mode):
    p = Pen(mode)
    # anel de engrenagem
    p.line(gear_points(CX, CY, RING, RING * 0.86), 2.6 * SS, closed=True)

    has_sym = n in SYMBOLS
    digits = len(str(n))
    if has_sym:
        size = RING * (0.95 if digits == 1 else 0.74)
        p.text((CX, CY - RING * 0.43), str(n), size)
        unit, dy = SYM_LAYOUT[n]
        SYMBOLS[n](p, CX, CY + RING * dy, RING * unit)
    else:
        size = RING * (1.45 if digits == 1 else 1.02)
        p.text((CX, CY), str(n), size)

    # 6 e 9 recebem um ponto para nao confundir
    if n in (6, 9) and not has_sym:
        r = 2.6 * SS
        y = CY + RING * 0.82
        p.ellipse((CX - r, y - r, CX + r, y + r), filled=True)

    return p.img.resize((FINAL, FINAL), Image.LANCZOS)


def main():
    tiles = []
    for n in range(1, 21):
        color = render(n, "color")
        bump = render(n, "bump").convert("L")
        color.save(os.path.join(FACES, f"d20_{n:02d}.png"))
        bump.save(os.path.join(FACES, f"d20_{n:02d}_bump.png"))
        tiles.append(color)

    # folha de contato: faces sobre fundo de aco, com a silhueta do triangulo
    cols, rows = 5, 4
    sheet = Image.new("RGB", (cols * FINAL, rows * FINAL), (142, 153, 164))
    for i, t in enumerate(tiles):
        x, y = (i % cols) * FINAL, (i // cols) * FINAL
        bg = Image.new("RGBA", (FINAL, FINAL), (142, 153, 164, 255))
        d = ImageDraw.Draw(bg)
        m = 4
        tri = [(FINAL / 2, m), (FINAL - m, FINAL - m), (m, FINAL - m)]
        d.line(tri + [tri[0]], fill=(80, 90, 100, 255), width=2)
        bg.alpha_composite(t)
        sheet.paste(bg.convert("RGB"), (x, y))
    sheet.save(os.path.join(OUT, "preview.png"))
    print("ok:", len(tiles), "faces")


if __name__ == "__main__":
    main()
