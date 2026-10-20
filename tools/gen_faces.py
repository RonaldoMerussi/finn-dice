#!/usr/bin/env python3
"""Gera as faces do kit de dados do Finn "Orelha-de-Prata" para o Dice So Nice.

Dados com imagem: d6, d8, d10, d12, d20 e d100 (dezenas).
O d4 usa texto (o Dice So Nice desenha 3 números por face, então não usamos imagem).

Saída (pasta passada como argumento, padrão "assets"):
  faces/<dado>_NN.png         cor, fundo transparente, 256x256
  faces/<dado>_NN_bump.png    relevo (branco = alto)
  preview.png                 folha de contato para conferir

Ajustes rápidos (se a face ficar grande ou pequena no Foundry):
  em DICE, mude "ring" (raio da engrenagem, fração do lado) e "cy" (centro vertical).
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
FACES = os.path.join(OUT, "faces")
os.makedirs(FACES, exist_ok=True)

FINAL = 256            # tamanho final do PNG (o Dice So Nice pede 256x256)
SS = 2                 # supersampling para suavizar as bordas
S = FINAL * SS
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
WHITE = (255, 255, 255, 255)

# cores das imagens (as mesmas dos colorsets do módulo)
PALETTES = {
    "steel": {"fill": (201, 162, 75, 255), "outline": (27, 31, 38, 255), "bg": (142, 153, 164)},
    "brass": {"fill": (27, 42, 74, 255), "outline": (243, 227, 179, 255), "bg": (201, 162, 75)},
    "ember": {"fill": (255, 179, 71, 255), "outline": (26, 15, 8, 255), "bg": (74, 47, 26)},
}


class Pen:
    """Desenha em dois modos: cor (preenchimento com contorno) e bump (branco sobre preto)."""

    def __init__(self, mode, palette, cx, cy, ring):
        self.mode = mode
        self.fill = palette["fill"]
        self.outline = palette["outline"]
        self.cx, self.cy, self.ring = cx, cy, ring
        bg = (0, 0, 0, 0) if mode == "color" else (0, 0, 0, 255)
        self.img = Image.new("RGBA", (S, S), bg)
        self.d = ImageDraw.Draw(self.img)

    def line(self, pts, w, closed=False):
        if closed:
            pts = list(pts) + [pts[0]]
        if self.mode == "color":
            self.d.line(pts, fill=self.outline, width=int(w + 7 * SS), joint="curve")
            self.d.line(pts, fill=self.fill, width=int(w), joint="curve")
        else:
            self.d.line(pts, fill=WHITE, width=int(w), joint="curve")

    def ellipse(self, box, w=0, filled=False):
        x0, y0, x1, y1 = box
        if self.mode == "color":
            pad = 3.5 * SS
            self.d.ellipse((x0 - pad, y0 - pad, x1 + pad, y1 + pad), fill=self.outline)
            self.d.ellipse(box, fill=self.fill if filled else (0, 0, 0, 0))
            if not filled:
                self.d.arc(box, 0, 360, fill=self.fill, width=int(w))
        else:
            if filled:
                self.d.ellipse(box, fill=WHITE)
            else:
                self.d.arc(box, 0, 360, fill=WHITE, width=int(w))

    def text(self, xy, txt, size):
        font = ImageFont.truetype(FONT_PATH, int(size))
        if self.mode == "color":
            self.d.text(xy, txt, font=font, fill=self.fill, anchor="mm",
                        stroke_width=int(3.5 * SS), stroke_fill=self.outline)
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


# ---------- símbolos pequenos, desenhados abaixo do número ----------
def sym_string(p, cx, cy, u):
    """corda partida (1 do d20)."""
    p.line([(cx - 0.25 * u, cy - 1.4 * u), (cx - 0.25 * u, cy - 0.2 * u)], 0.34 * u)
    p.line([(cx + 0.25 * u, cy + 0.35 * u), (cx + 0.25 * u, cy + 1.4 * u)], 0.34 * u)
    p.line([(cx - 0.25 * u, cy - 0.2 * u), (cx + 0.2 * u, cy + 0.05 * u),
            (cx + 0.7 * u, cy - 0.25 * u), (cx + 0.9 * u, cy - 0.7 * u)], 0.28 * u)


def sym_note(p, cx, cy, u):
    """nota musical (Inspiração Bárdica e 5 do d20)."""
    p.ellipse((cx - 0.9 * u, cy + 0.25 * u, cx - 0.05 * u, cy + 0.95 * u), filled=True)
    p.line([(cx - 0.12 * u, cy + 0.6 * u), (cx - 0.12 * u, cy - 1.0 * u)], 0.2 * u)
    p.line([(cx - 0.12 * u, cy - 1.0 * u), (cx + 0.7 * u, cy - 0.5 * u),
            (cx + 0.5 * u, cy + 0.1 * u)], 0.2 * u)


def sym_clock(p, cx, cy, u):
    """relógio (10 do d20)."""
    p.ellipse((cx - u, cy - u, cx + u, cy + u), w=0.2 * u)
    p.line([(cx, cy), (cx, cy - 0.65 * u)], 0.18 * u)
    p.line([(cx, cy), (cx + 0.45 * u, cy + 0.15 * u)], 0.18 * u)


def sym_gear(p, cx, cy, u):
    """engrenagem (15 do d20)."""
    p.line(gear_points(cx, cy, u, 0.7 * u, teeth=8), 0.17 * u, closed=True)
    p.ellipse((cx - 0.28 * u, cy - 0.28 * u, cx + 0.28 * u, cy + 0.28 * u), filled=True)


def sym_lute(p, cx, cy, u):
    """alaúde (20 do d20)."""
    p.line([(cx, cy - 1.0 * u), (cx, cy - 2.2 * u)], 0.42 * u)
    p.line([(cx - 0.5 * u, cy - 2.2 * u), (cx + 0.5 * u, cy - 2.35 * u)], 0.34 * u)
    p.ellipse((cx - 1.0 * u, cy - 1.2 * u, cx + 1.0 * u, cy + 1.2 * u), w=0.34 * u)
    p.ellipse((cx - 0.3 * u, cy - 0.3 * u, cx + 0.3 * u, cy + 0.3 * u), filled=True)


SYM_FUNCS = {"string": sym_string, "note": sym_note, "clock": sym_clock,
             "gear": sym_gear, "lute": sym_lute}
# (unidade em fração do anel, deslocamento vertical em fração do anel)
SYM_LAYOUT = {"string": (0.26, 0.47), "note": (0.27, 0.50), "clock": (0.27, 0.50),
              "gear": (0.27, 0.50), "lute": (0.25, 0.50)}


def nums(a, b):
    return [str(i) for i in range(a, b + 1)]


DICE = {
    # d6: dano de Bola de Fogo (8d6), bronze com números cor de brasa
    "d6": dict(labels=nums(1, 6), palette="ember", ring=0.40, cy=0.50, symbols={}),
    # d8: Inspiração Bárdica (nível 5 a 9), latão com números azul-marinho e nota musical
    "d8": dict(labels=nums(1, 8), palette="brass", ring=0.315, cy=0.575,
               symbols={str(i): "note" for i in range(1, 9)}),
    # d10: a face "0" vale 10 (ordem de valor: 1..9 e depois 0)
    "d10": dict(labels=nums(1, 9) + ["0"], palette="steel", ring=0.29, cy=0.52, symbols={}),
    "d12": dict(labels=nums(1, 12), palette="steel", ring=0.34, cy=0.50, symbols={}, two=0.86),
    "d20": dict(labels=nums(1, 20), palette="steel", ring=0.315, cy=0.575,
                symbols={"1": "string", "5": "note", "10": "clock", "15": "gear", "20": "lute"}),
    # d100 (dezenas): 10..90 e "00" por último
    "d100": dict(labels=[str(i * 10) for i in range(1, 10)] + ["00"], palette="steel",
                 ring=0.29, cy=0.52, symbols={}),
}


def render(cfg, label, mode):
    pal = PALETTES[cfg["palette"]]
    R = S * cfg["ring"]
    p = Pen(mode, pal, S * 0.5, S * cfg["cy"], R)
    cx, cy = p.cx, p.cy

    # anel de engrenagem
    p.line(gear_points(cx, cy, R, R * 0.86), 2.6 * SS, closed=True)

    sym = cfg["symbols"].get(label)
    digits = len(label)
    if sym:
        size = R * (0.95 if digits == 1 else 0.74)
        p.text((cx, cy - R * 0.43), label, size)
        unit, dy = SYM_LAYOUT[sym]
        SYM_FUNCS[sym](p, cx, cy + R * dy, R * unit)
    else:
        size = R * (1.45 if digits == 1 else cfg.get("two", 1.02))
        p.text((cx, cy), label, size)
        # 6 e 9 recebem um ponto para não confundir
        if label in ("6", "9"):
            r = 2.6 * SS
            y = cy + R * 0.82
            p.ellipse((cx - r, y - r, cx + r, y + r), filled=True)

    return p.img.resize((FINAL, FINAL), Image.LANCZOS)


def main():
    rows = []
    for die, cfg in DICE.items():
        tiles = []
        for i, label in enumerate(cfg["labels"], start=1):
            color = render(cfg, label, "color")
            bump = render(cfg, label, "bump").convert("L")
            color.save(os.path.join(FACES, f"{die}_{i:02d}.png"))
            bump.save(os.path.join(FACES, f"{die}_{i:02d}_bump.png"))
            tiles.append(color)
        rows.append((die, cfg, tiles))
        print(f"{die}: {len(tiles)} faces")

    # folha de contato: 10 colunas, miniaturas de 128px, fundo na cor do colorset
    th, cols = 128, 10
    total_rows = sum(math.ceil(len(t) / cols) for _, _, t in rows)
    sheet = Image.new("RGB", (cols * th, total_rows * th), (40, 40, 40))
    y = 0
    for die, cfg, tiles in rows:
        bgc = PALETTES[cfg["palette"]]["bg"]
        for i, t in enumerate(tiles):
            x = (i % cols) * th
            yy = y + (i // cols) * th
            bg = Image.new("RGBA", (th, th), bgc + (255,))
            ImageDraw.Draw(bg).rectangle((0, 0, th - 1, th - 1), outline=(30, 30, 30, 255))
            bg.alpha_composite(t.resize((th, th), Image.LANCZOS))
            sheet.paste(bg.convert("RGB"), (x, yy))
        y += math.ceil(len(tiles) / cols) * th
    sheet.save(os.path.join(OUT, "preview.png"))
    print("ok")


if __name__ == "__main__":
    main()
