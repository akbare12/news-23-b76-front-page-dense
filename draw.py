#!/usr/bin/env python3
"""news-23 b76 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, font):
    return draw.textlength(text, font=font)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, label, color):
    f = F(SANSB, 9)
    w = int(tw(draw, label, f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=color)
    draw.text((x + 5, y + 2), label, font=f, fill="white")
    return w


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 56], fill=(12, 12, 12))
    d.text((10, 6), "THE WORLD TODAY", font=F(SERIF, 42), fill="white")
    d.text((W - 10 - tw(d, "MONDAY 23 NOVEMBER 2026", F(SANSB, 17)),
            20), "MONDAY 23 NOVEMBER 2026", font=F(SANSB, 17), fill=(212, 175, 55))

    # ---------- kicker ----------
    d.rectangle([0, 56, W, 74], fill=(122, 20, 20))
    d.text((10, 60), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
           font=F(SANSB, 12), fill="white")

    # ---------- number strip (2 rows x 5) ----------
    strip = [
        [("-3.3%", "KOSPI", (178, 34, 34)), ("5.3", "US-CHINA POWER GAP", (20, 60, 140)),
         ("11,762", "EBOLA CASES, DRC", (20, 110, 60)), ("10T won", "SEOUL STABILISATION FUND", (140, 100, 20)),
         ("2%", "BILLIONAIRE TAX IN PARIS", (110, 40, 140))],
        [("$450M", "SKUBAL DEAL", (20, 60, 140)), ("165", "RUSSIAN MISSILES/WEEK", (178, 34, 34)),
         ("12,000", "CLEARED IN MANCHESTER", (20, 110, 60)), ("264 kg", "EXPLOSIVES SEIZED", (140, 100, 20)),
         ("$107.3B", "ANTHROPIC IPO", (110, 40, 140))],
    ]
    cell = 1024 // 5
    for r, row in enumerate(strip):
        yv = 75 + r * 30
        for c, (val, lab, col) in enumerate(row):
            x = c * cell + 8
            d.text((x, yv), val, font=F(SANSB, 19), fill=col)
            d.text((x, yv + 21), lab, font=F(SANS, 9), fill=(90, 90, 90))

    # ---------- region bar ----------
    regs = [("ASIA-PACIFIC 7", (20, 80, 180), 228), ("AMERICAS 8", (178, 34, 34), 260),
            ("MIDDLE EAST 6", (180, 140, 20), 195), ("EUROPE 5", (0, 130, 120), 163),
            ("AFRICA 3", (110, 40, 140), 98), ("WORLD 2", (40, 40, 90), 64)]
    x = 0
    for name, col, w in regs:
        d.rectangle([x, 138, x + w, 156], fill=col)
        d.text((x + 6, 142), name, font=F(SANSB, 11), fill="white")
        x += w

    # ---------- UTC strip ----------
    d.text((10, 159), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
           font=F(SANS, 10), fill=(90, 90, 90))
    d.text((W - 10 - tw(d, "~ APPROX", F(SANS, 10)), 159), "~ APPROX", font=F(SANS, 10), fill=(90, 90, 90))

    # ---------- hero scenes ----------
    HX = [8, 348, 688]
    HW = 328
    # scene 1: Kospi skyline + chart
    x0 = HX[0]
    d.rectangle([x0, 170, x0 + HW, 270], fill=(10, 22, 52))
    import random
    random.seed(7)
    for bx in range(x0 + 8, x0 + HW - 8, 26):
        bh = random.randint(30, 78)
        d.rectangle([bx, 268 - bh, bx + 20, 268], fill=(22, 38, 78))
        for wy in range(268 - bh + 5, 264, 12):
            for wx in (bx + 4, bx + 12):
                if random.random() < 0.6:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    pts = [(x0 + 14, 246), (x0 + 60, 226), (x0 + 105, 236), (x0 + 150, 208),
           (x0 + 195, 218), (x0 + 240, 190), (x0 + 285, 200), (x0 + 316, 178)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 200, 120), outline=(255, 140, 40))
    d.text((x0 + 8, 176), "-3.3%", font=F(SANSB, 26), fill=(255, 70, 60))
    # scene 2: Guterres globe
    x0 = HX[1]
    d.rectangle([x0, 170, x0 + HW, 270], fill=(0, 110, 100))
    d.text((x0 + 10, 178), "150 DELEGATES", font=F(SANSB, 25), fill=(255, 210, 90))
    d.text((x0 + 10, 206), "BACK A RISK", font=F(SANSB, 25), fill=(255, 210, 90))
    d.text((x0 + 10, 234), "FRAMEWORK", font=F(SANSB, 25), fill=(255, 210, 90))
    gx, gy, gr = x0 + 272, 222, 40
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(170, 225, 215))
    for a in (-28, -14, 0, 14, 28):
        d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 90 + a * 2, 270 - a * 2, fill=(0, 110, 100), width=1)
    d.ellipse([gx - 14, gy - gr, gx + 14, gy + gr], outline=(0, 110, 100), width=1)
    d.line([gx - gr, gy, gx + gr, gy], fill=(0, 110, 100), width=1)
    d.line([gx - gr + 8, gy - 22, gx + gr - 8, gy - 22], fill=(0, 110, 100), width=1)
    d.line([gx - gr + 8, gy + 22, gx + gr - 8, gy + 22], fill=(0, 110, 100), width=1)
    # scene 3: Power Index bars
    x0 = HX[2]
    d.rectangle([x0, 170, x0 + HW, 270], fill=(250, 244, 222))
    d.text((x0 + 8, 174), "NARROWEST SINCE 2018", font=F(SANSB, 11), fill=(90, 70, 20))
    d.text((x0 + HW - 8 - tw(d, "GAP 5.3", F(SANSB, 11)), 174), "GAP 5.3", font=F(SANSB, 11), fill=(178, 34, 34))
    bars = [("78.9", "US", (20, 40, 110), 62), ("73.6", "CHINA", (178, 34, 34), 58),
            ("40.5", "INDIA", (200, 160, 40), 34)]
    bx = x0 + 22
    for val, lab, col, bh in bars:
        d.text((bx + 18, 196), val, font=F(SANSB, 16), fill=(30, 30, 30))
        d.rectangle([bx, 216, bx + 72, 216 + bh], fill=col)
        d.text((bx + 26, 216 + bh - 18), lab, font=F(SANSB, 11), fill="white")
        bx += 100
    # black source strips under scenes
    strips = ["KOSPI 4,708.54  ·  -161 PTS", "UN  ·  BRIDGETOWN", "ASIA POWER INDEX 2026"]
    for i, s in enumerate(strips):
        d.rectangle([HX[i], 270, HX[i] + HW, 286], fill=(12, 12, 12))
        d.text((HX[i] + 8, 273), s, font=F(SANSB, 11), fill="white")

    # ---------- hero headlines / bodies / source+chip ----------
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    for i, (hl, body, src) in enumerate(heroes):
        x = HX[i]
        lines = wrap(d, hl, F(SANSB, 20), HW)
        y = 290
        for ln in lines[:2]:
            d.text((x, y), ln, font=F(SANSB, 20), fill=(15, 15, 15))
            y += 22
        blines = wrap(d, body, F(SANS, 12), HW)
        by = 336
        for ln in blines[:2]:
            d.text((x, by), ln, font=F(SANS, 12), fill=(40, 40, 40))
            by += 14
        d.text((x, 366), src, font=F(SANS, 10), fill=(110, 110, 110))
        chip(d, x + HW - 62, 364, "REPORTED", (30, 90, 170))

    # ---------- MORE OF THE DAY bar ----------
    d.rectangle([0, 382, W, 400], fill=(12, 12, 12))
    d.text((10, 386), "MORE OF THE DAY  —  10 STORIES", font=F(SANSB, 13), fill="white")

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", (178, 34, 34), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", (30, 90, 170)),
        ("FBI", (30, 50, 110), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", (30, 90, 170)),
        ("WHITE HOUSE", (150, 110, 20), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", (30, 90, 170)),
        ("MARKETS", (0, 130, 120), "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", (30, 90, 170)),
        ("SPORT", (200, 30, 50), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", (30, 90, 170)),
        ("SPORT", (200, 30, 50), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", (30, 90, 170)),
        ("LEGAL", (110, 40, 140), "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", (30, 90, 170)),
        ("TECH", (20, 80, 180), "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", (30, 90, 170)),
        ("EUROPE", (20, 130, 60), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", (178, 34, 34)),
        ("SPACE", (90, 40, 120), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", (178, 34, 34)),
    ]
    cw = (W - 16 - 4 * 6) // 5  # 5 cols, 6px gaps, 8px margins
    for idx, (cat, ccol, hl, body, src, tag, tcol) in enumerate(cards):
        r, c = divmod(idx, 5)
        x = 8 + c * (cw + 6)
        y = 400 + r * 78
        d.rectangle([x, y, x + cw, y + 16], fill=ccol)
        d.text((x + 5, y + 2), cat, font=F(SANSB, 10), fill="white")
        d.text((x + cw - 5 - tw(d, str(idx + 1), F(SANSB, 10)), y + 2), str(idx + 1),
               font=F(SANSB, 10), fill="white")
        lines = wrap(d, hl, F(SANSB, 13), cw - 6)
        ly = y + 19
        for ln in lines[:2]:
            d.text((x + 3, ly), ln, font=F(SANSB, 13), fill=(15, 15, 15))
            ly += 15
        d.text((x + 3, y + 50), body, font=F(SANS, 10), fill=(60, 60, 60))
        d.text((x + 3, y + 63), src, font=F(SANS, 9), fill=(110, 110, 110))
        chip(d, x + cw - 62, y + 62, tag, tcol)

    # ---------- map + ALSO header ----------
    d.rectangle([0, 560, W, 578], fill=(12, 12, 12))
    d.text((10, 564), "WHERE IT HAPPENED", font=F(SANSB, 13), fill="white")
    d.text((348, 564), "ALSO ON MONDAY", font=F(SANSB, 13), fill="white")

    # ---------- map ----------
    d.rectangle([8, 578, 340, 868], outline=(180, 180, 180), width=1)
    # continent blobs (stylised)
    d.polygon([(20, 620), (90, 600), (150, 615), (140, 700), (110, 780), (60, 770), (25, 700)],
              fill=(200, 230, 190))  # Americas
    d.polygon([(170, 600), (260, 590), (330, 610), (320, 680), (250, 700), (180, 680)],
              fill=(200, 230, 190))  # Eurasia
    d.polygon([(180, 720), (250, 715), (265, 780), (210, 800), (175, 760)],
              fill=(200, 230, 190))  # Africa
    d.ellipse([285, 790, 325, 815], fill=(200, 230, 190))  # Australia
    pins = [(285, 640, 1), (60, 760, 2), (300, 620, 3), (95, 680, 4), (120, 665, 5),
            (215, 640, 6), (85, 705, 7), (55, 715, 8), (100, 735, 9), (110, 755, 10),
            (235, 635, 11), (195, 630, 12), (255, 625, 13)]
    pf = F(SANSB, 10)
    for px, py, n in pins:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(200, 30, 40), outline="white", width=1)
        t = str(n)
        d.text((px - tw(d, t, pf) / 2, py - 7), t, font=pf, fill="white")
    d.text((16, 800), "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing", font=F(SANS, 10), fill=(60, 60, 60))
    d.text((16, 816), "4 Washington · 5 New York · 6 Kyiv · 7 Chicago · 8 SF", font=F(SANS, 10), fill=(60, 60, 60))
    d.text((16, 832), "9 Denver · 10 Austin · 11 Warsaw · 12 London · 13 Moscow", font=F(SANS, 10), fill=(60, 60, 60))

    # ---------- ALSO list ----------
    also = [
        (14, "Paris: 100+ back 2% billionaire tax", False),
        (15, "Manchester: 12,000 cleared", False),
        (16, "Zelenskyy: 165 missiles in a week", False),
        (17, "COP31: the day after pact rejected", False),
        (18, "Benghazi: UN demands port probe", True),
        (19, "Israel unity talks resume", False),
        (20, "Gaza: two killed in Israeli strike", False),
        (21, "West Bank settler attacks", False),
        (22, "Iran war: no deal in sight", False),
        (23, "Lebanon seizes 264 kg explosives", False),
        (24, "Bahrain: strike hits plant, 2 hurt", False),
        (25, "Sudan: defences down drones", True),
        (26, "DRC: fighting traps Ebola teams", False),
        (27, "Bangladesh: Hasina jailed if she returns", False),
        (28, "Seoul minister quits in exam row", False),
        (29, "SK Telecom -7.3% as hype cools", False),
        (30, "China eases margin rules", False),
        (31, "Seoul readies 10T-won fund", False),
    ]
    af = F(SANS, 12)
    for i, (n, txt, claim) in enumerate(also):
        col, row = divmod(i, 9)
        x = 348 + col * 340
        y = 584 + row * 31
        s = f"{n}. {txt}"
        if claim:
            s += "  [CLAIM]"
        d.text((x, y), s, font=af, fill=(30, 30, 30) if not claim else (150, 20, 20))

    # ---------- DATE CHECK ----------
    d.rectangle([8, 872, 1016, 936], outline=(200, 30, 40), width=2)
    d.text((16, 876), "DATE CHECK", font=F(SANSB, 13), fill=(200, 30, 40))
    rt = "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY"
    d.text((1016 - 8 - tw(d, rt, F(SANSB, 10)), 879), rt, font=F(SANSB, 10), fill=(200, 30, 40))
    d.text((16, 894), "LEFT OUT — NOT 23 NOV: Dems 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo (22 Nov) · EU–Indonesia (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar (19 Nov)",
           font=F(SANS, 11), fill=(30, 30, 30))
    d.text((16, 912), "NOT YET — Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
           font=F(SANS, 11), fill=(30, 30, 30))

    # ---------- footer ----------
    d.rectangle([0, 940, W, H], fill=(12, 12, 12))
    d.text((10, 946), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=F(SANS, 10), fill=(200, 200, 200))
    d.text((10, 962), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
           font=F(SANS, 10), fill=(200, 200, 200))
    d.text((10, 978), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=F(SANS, 10), fill=(200, 200, 200))
    ft = "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions"
    d.text(((W - tw(d, ft, F(SANSB, 12))) / 2, 998), ft, font=F(SANSB, 12), fill=(212, 175, 55))

    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT))


if __name__ == "__main__":
    main()
