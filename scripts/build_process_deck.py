#!/usr/bin/env python3
# ruff: noqa: E501  (в файле намеренно длинные строки HTML/CSS/JS-шаблонов)
"""Генератор колоды: docs/process_defense.html.

Что делает:
  * берёт <head> (стили и встроенные шрифты) из docs/defense.html — автономность
    сохраняется, внешние CDN не добавляются;
  * титульный лист: «AquaPredict — предиктивная надстройка над «БИТ:LIMS»»;
  * слайды 2 и 3 — содержание раздела 5 доклада (process_report.md),
    отрендеренное из первоисточника;
  * далее — полный текст артефактов Vision and Scope, glossary, stakeholder_map,
    use_cases и слайд с полным перечнем артефактов;
  * далее — Договор и ТЗ (полный текст), затем экранные формы SCR-01…12 и
    презентация Заказчика.

Запуск (из корня репозитория):
    .venv/bin/python scripts/build_process_deck.py

После изменения docs/system_analysis/legal/contract_draft.md, tz_draft.md,
process_report.md или любого из встроенных артефактов перезапустите скрипт,
чтобы колода не показывала устаревший текст.

Замечание: подчёркивания-заполнители вида `___` экранируются перед рендерингом,
иначе Markdown трактует их как выделение (emphasis). Не удаляйте эту защиту.
"""

import html as _html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SA = DOCS / "system_analysis"
DEFENSE = DOCS / "defense.html"
CONTRACT = SA / "legal/contract_draft.md"
TZ = SA / "legal/tz_draft.md"
REPORT = SA / "process_report.md"
OUT = DOCS / "process_defense.html"

ARTIFACT_DOCS = [
    ("Vision and Scope", SA / "01_vision_and_scope.md"),
    ("Glossary", SA / "02_glossary.md"),
    ("Stakeholder Map", SA / "03_stakeholder_map.md"),
    ("Use Cases", SA / "04_use_cases.md"),
]

head = DEFENSE.read_text(encoding="utf-8").split("<body>", 1)[0]
head = head.replace(
    "<title>AquaPredict — защита проекта</title>",
    "<title>AquaPredict — предиктивная надстройка над «БИТ:LIMS»</title>",
)

md_ext = ["tables", "fenced_code", "sane_lists", "attr_list"]


def render_md(text: str) -> str:
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00C{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]*)`", stash, text)
    text = text.replace("_", "\\_")
    out = markdown.markdown(text, extensions=md_ext)
    for idx, val in enumerate(codes):
        out = out.replace(f"\x00C{idx}\x00", f"<code>{_html.escape(val)}</code>")
    return out


def md_html(path: Path) -> str:
    return render_md(path.read_text(encoding="utf-8"))


def report_section(num: int) -> str:
    """Тело раздела «## <num>. ...» из process_report.md (без заголовка)."""
    text = REPORT.read_text(encoding="utf-8")
    m = re.search(rf"^##\s*{num}\..*?(?=^##\s*{num + 1}\.)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"раздел {num} не найден в {REPORT}")
    body = re.sub(rf"^##\s*{num}\.[^\n]*\n", "", m.group(0), count=1)
    return body.strip()


def report_heading(num: int) -> str:
    """Заголовок раздела «## <num>. ...» из process_report.md."""
    text = REPORT.read_text(encoding="utf-8")
    m = re.search(rf"^##\s*{num}\.\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else f"Раздел {num}"


contract_html = md_html(CONTRACT)
tz_html = md_html(TZ)

# Раздел 5 доклада — двумя слайдами: (а) проблема и ручной процесс,
# (б) преимущества и проблемы внедрения ИИ.
sec5 = report_section(5)
_split = sec5.find("Поэтому целесообразно")
if _split < 0:
    raise SystemExit("не найден маркер деления раздела 5")
sec5_a = sec5[:_split].strip()
sec5_b = sec5[_split:].strip()

EXTRA_CSS = """
  .docSlide{padding:4vh 6vw}
  .doc{max-width:90ch;font-size:15px;line-height:1.6}
  .doc h1{font-size:24px;margin:.2em 0 .5em}
  .doc h2{font-size:19px;margin:1.2em 0 .4em;color:var(--accent)}
  .doc h3{font-size:16px;margin:1em 0 .3em}
  .doc p{margin:.5em 0}
  .doc ul,.doc ol{display:block;max-width:none;gap:0;margin:.5em 0;padding-left:1.4em}
  .doc ul li,.doc ol li{padding-left:0;font-size:15px;list-style:disc;margin:.25em 0}
  .doc ul li::before{content:none}
  .doc ol li{list-style:decimal}
  .doc blockquote{margin:.6em 0;padding:8px 14px;border-left:3px solid var(--accent);background:var(--accent-soft);color:var(--fg);border-radius:0 8px 8px 0}
  .doc table{border-collapse:collapse;width:100%;margin:.7em 0;font-size:13.5px}
  .doc th,.doc td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
  .doc th{background:var(--accent-soft);color:var(--accent);font-weight:700}
  .doc code{background:var(--accent-soft);color:var(--accent);border-radius:5px;padding:1px 5px}
  .doc hr{border:none;border-top:1px solid var(--line);margin:1.2em 0}
  .docScrollHint{font-size:13px;color:var(--muted);margin:0 0 6px}
  .artifacts{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin-top:8px}
  .artifacts .card{padding:12px 14px}
  .artifacts h3{margin:0 0 6px;font-size:14px}
  .artifacts ul{display:block;max-width:none;gap:0;margin:0;padding:0}
  .artifacts li{list-style:none;padding-left:0;font-size:12.5px;line-height:1.45;margin:1px 0;color:var(--muted)}
  .artifacts li::before{content:none}
"""


def slide(inner: str, extra_class: str = "") -> str:
    cls = "slide" + (f" {extra_class}" if extra_class else "")
    return f'  <section class="{cls}">\n{inner}\n  </section>\n'


def artifact_deck() -> str:
    """Полный перечень артефактов: обход docs/system_analysis и группировка."""
    groups: list[tuple[str, str]] = [
        ("Ядро системного анализа", ""),
        ("Требования", "requirements"),
        ("Диаграммы", "diagrams"),
        ("План реализации", "plans"),
        ("Бэклог", "backlog"),
        ("Контроль качества", "qa"),
        ("Право", "legal"),
        ("Экономика", "cost"),
        ("Руководства", "manuals"),
        ("Рецензии и обзоры", "reviews"),
    ]
    cards = []
    for title, sub in groups:
        base = SA / sub if sub else SA
        items: list[str] = []
        if sub == "":
            items = sorted(p.name for p in base.iterdir() if p.is_file())
        else:
            for p in sorted(base.iterdir()):
                if p.is_file():
                    items.append(p.name)
                elif p.is_dir():
                    for q in sorted(p.rglob("*")):
                        if q.is_file():
                            items.append(str(q.relative_to(base)))
        if items:
            lis = "".join(f"<li>{_html.escape(i)}</li>" for i in items)
            cards.append(f'<div class="card"><h3>{_html.escape(title)}</h3><ul>{lis}</ul></div>')
    return '<div class="artifacts">' + "".join(cards) + "</div>"


slides = []

slides.append(slide(
    '''    <div class="kicker">Защита проекта · системный анализ</div>
    <h1>AquaPredict — предиктивная надстройка над «БИТ:LIMS»</h1>
    <p style="margin-top:26px;font-size:15px;color:#8fb3bd">Авторы: Баева Анастасия Сергеевна · Волков Игорь Анатольевич</p>''',
    "titleSlide active"))

slides.append(slide(
    '    <p class="eyebrow">Доклад · раздел 5</p>'
    '<h2 class="slideTitle">Проблема, которую мы взялись закрыть</h2>'
    f'<div class="doc">{render_md(sec5_a)}</div>',
    "docSlide"))

slides.append(slide(
    '    <p class="eyebrow">Доклад · раздел 5 (продолжение)</p>'
    '<h2 class="slideTitle">Преимущества и проблемы внедрения ИИ</h2>'
    f'<div class="doc">{render_md(sec5_b)}</div>',
    "docSlide"))

for _num in (7, 8):
    slides.append(slide(
        f'    <p class="eyebrow">Доклад · раздел {_num}</p>'
        f'<h2 class="slideTitle">{_html.escape(report_heading(_num))}</h2>'
        f'<div class="doc">{render_md(report_section(_num))}</div>',
        "docSlide"))

for label, path in ARTIFACT_DOCS:
    slides.append(slide(
        f'    <p class="eyebrow">Артефакт · {_html.escape(label)}</p>'
        f'<h2 class="slideTitle">Полный текст: {_html.escape(label)}</h2>'
        f'<p class="docScrollHint">Источник: <code>docs/system_analysis/{_html.escape(path.name)}</code>. Прокрутите страницу, чтобы прочитать полностью.</p>'
        f'<div class="doc">{md_html(path)}</div>',
        "docSlide"))

slides.append(slide(
    '    <p class="eyebrow">Артефакты проекта</p>'
    '<h2 class="slideTitle">Полный перечень артефактов</h2>'
    '<p class="docScrollHint">Все артефакты репозитория (<code>docs/system_analysis/</code>).</p>'
    + artifact_deck(),
    "docSlide"))

slides.append(slide(
    '    <p class="eyebrow">Документы · Договор</p>'
    '<h2 class="slideTitle">Полный текст Договора</h2>'
    '<p class="docScrollHint">Проект договора на выполнение работ с приложениями № 2–5. Прокрутите страницу, чтобы прочитать полностью.<br>'
    'Источник: <code>docs/system_analysis/legal/contract_draft.md</code> (ред. 2.2, 2026-10-13). Колода собрана из него; при правке документа перезапустите '
    '<code>scripts/build_process_deck.py</code>.</p>'
    f'<div class="doc">{contract_html}</div>',
    "docSlide"))

slides.append(slide(
    '    <p class="eyebrow">Документы · ТЗ</p>'
    '<h2 class="slideTitle">Полный текст Технического задания</h2>'
    '<p class="docScrollHint">Техническое задание (структура по ГОСТ 34.602-89) с приложениями А и Б. Прокрутите страницу, чтобы прочитать полностью.<br>'
    'Источник: <code>docs/system_analysis/legal/tz_draft.md</code> (ред. 1.2, 2026-10-13). Колода собрана из него; при правке документа перезапустите '
    '<code>scripts/build_process_deck.py</code>.</p>'
    f'<div class="doc">{tz_html}</div>',
    "docSlide"))

mockups = [
    ("SCR-01", "Дашборд технолога", "scr01_dashboard.html"),
    ("SCR-02", "Карточка инцидента и вердикт", "scr02_incident.html"),
    ("SCR-03", "Задачи (корректирующее действие / отбор)", "scr03_tasks.html"),
    ("SCR-04", "Производственная партия", "scr04_party.html"),
    ("SCR-05", "Протоколы испытаний (read-only)", "scr05_protocols.html"),
    ("SCR-06", "Метрики модели", "scr06_metrics.html"),
    ("SCR-07", "MLOps — модели и версии", "scr07_mlops.html"),
    ("SCR-08", "Cold Start", "scr08_coldstart.html"),
    ("SCR-09", "Здоровье телеметрии", "scr09_telemetry_health.html"),
    ("SCR-10", "Журнал аудита", "scr10_audit.html"),
    ("SCR-11", "Администрирование (рабочая точка)", "scr11_admin.html"),
    ("SCR-12", "Уведомления", "scr12_notifications.html"),
]
for code, title, fname in mockups:
    slides.append(slide(
        f'    <p class="eyebrow">Экран · {code}</p><h2 class="slideTitle">{title}</h2>'
        f'<iframe class="frame" src="mockups/{fname}" title="{code}" loading="lazy"></iframe>'
    ))

slides.append(slide(
    '    <p class="eyebrow">Документы · для Заказчика</p>'
    '<h2 class="slideTitle">Презентация для Заказчика</h2>'
    '<p class="docScrollHint">Одностраничная презентация (прокрутите её внутри окна).</p>'
    '<iframe class="frame" style="height:74vh" src="system_analysis/presentation_customer.html" title="Презентация для Заказчика" loading="lazy"></iframe>'))

nav = '''
<div class="foot">AquaPredict · предиктивная надстройка над «БИТ:LIMS» · 2026 · <a href="https://github.com/igorvolk1961/water_checker">репозиторий</a></div>
<div class="controls">
  <button id="prev" aria-label="Назад">←</button>
  <span class="counter"><span id="cur">1</span> / <span id="total">20</span></span>
  <button id="next" aria-label="Вперёд">→</button>
</div>
<div class="progress" id="progress"></div>
<script>
  const slides=[...document.querySelectorAll('.slide')];
  let i=0;
  const cur=document.getElementById('cur'), total=document.getElementById('total'), bar=document.getElementById('progress');
  total.textContent=slides.length;
  function go(n){ i=Math.max(0,Math.min(slides.length-1,n)); slides.forEach((s,k)=>s.classList.toggle('active',k===i)); cur.textContent=i+1; bar.style.width=((i+1)/slides.length*100)+'%'; history.replaceState(null,'','#s'+(i+1)); }
  addEventListener('beforeprint',()=>{});
  document.getElementById('next').onclick=()=>go(i+1);
  document.getElementById('prev').onclick=()=>go(i-1);
  addEventListener('keydown',e=>{
    if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();go(i+1);}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(e.key)){e.preventDefault();go(i-1);}
    else if(e.key==='Home'){go(0);} else if(e.key==='End'){go(slides.length-1);}
    else if(e.key.toLowerCase()==='f'){ if(document.fullscreenElement)document.exitFullscreen(); else document.documentElement.requestFullscreen(); }
  });
  let x0=null;
  addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});
  addEventListener('touchend',e=>{ if(x0===null)return; const dx=e.changedTouches[0].clientX-x0; if(Math.abs(dx)>50) go(dx<0?i+1:i-1); x0=null; },{passive:true});
  const m=location.hash.match(/#s(\\d+)/); go(m?+m[1]-1:0);
</script>
'''

doc = (
    head
    + "<style>" + EXTRA_CSS + "</style>\n</head>\n<body>\n"
    + '<div class="deck" id="deck">\n\n'
    + "\n".join(slides)
    + "\n</div>\n"
    + nav
    + "</body>\n</html>\n"
)

OUT.write_text(doc, encoding="utf-8")
print("wrote", OUT, len(doc), "bytes;", len(slides), "slides")
