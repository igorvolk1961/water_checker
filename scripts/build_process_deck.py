#!/usr/bin/env python3
# ruff: noqa: E501  (в файле намеренно длинные строки HTML/CSS/JS-шаблонов)
"""Генератор колоды защиты о процессе: docs/process_defense.html.

Что делает:
  * берёт <head> (стили и встроенные шрифты) из docs/defense.html — автономность
    сохраняется, внешние CDN не добавляются;
  * собирает слайды процесса и материалы (макеты SCR-01…12, полный текст
    Договора и ТЗ, презентация для Заказчика);
  * встраивает полный текст legal/contract_draft.md и legal/tz_draft.md,
    отрендеренный из Markdown (таблицы, приложения).

Запуск (из корня репозитория):
    .venv/bin/python scripts/build_process_deck.py

После изменения docs/system_analysis/legal/contract_draft.md или tz_draft.md
перезапустите этот скрипт, чтобы колода не показывала устаревший текст.

Замечание: подчёркивания-заполнители вида `___` экранируются перед рендерингом,
иначе Markdown трактует их как выделение (emphasis). Не удаляйте эту защиту.
"""

import html as _html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEFENSE = DOCS / "defense.html"
CONTRACT = DOCS / "system_analysis/legal/contract_draft.md"
TZ = DOCS / "system_analysis/legal/tz_draft.md"
OUT = DOCS / "process_defense.html"

head = DEFENSE.read_text(encoding="utf-8").split("<body>", 1)[0]
head = head.replace(
    "<title>AquaPredict — защита проекта</title>",
    "<title>AquaPredict — процесс разработки (защита проекта)</title>",
)

md_ext = ["tables", "fenced_code", "sane_lists", "attr_list"]


def md_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
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


contract_html = md_html(CONTRACT)
tz_html = md_html(TZ)

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
"""


def slide(inner: str, extra_class: str = "") -> str:
    cls = "slide" + (f" {extra_class}" if extra_class else "")
    return f'  <section class="{cls}">\n{inner}\n  </section>\n'


slides = []

slides.append(slide('''    <div class="kicker">Защита проекта · системный анализ</div>
    <h1>Процесс, а не результат</h1>
    <p class="sub">Как мы за одни сутки смоделировали реальный проект: команда «человек + два ИИ-ассистента», распределение ролей, «LLM-as-a-Judge», глоссарий и references.</p>
    <div class="badges"><span>AquaPredict — предиктивная надстройка над «БИТ:LIMS»</span><span>Срок: 1 день</span><span>2026</span></div>
    <p class="sub" style="margin-top:18px">Авторы: Баева Анастасия Сергеевна · Волков Игорь Анатольевич</p>''', "titleSlide active"))

slides.append(slide('''    <p class="eyebrow">Контекст</p>
    <h2 class="slideTitle">Почему доклад — о процессе</h2>
    <ul>
      <li>Вчера мы слушали <b>красивые доклады</b> других слушателей — но мало полезные: про «почти готовый продукт», почти ничего — про то, <b>как</b> он делался.</li>
      <li>Преподаватель хвалил чужие проекты: «почти прод, принесут кучу денег».</li>
      <li>Сегодня — наш проект. Мы сознательно говорим <b>не о результатах, а о процессе разработки</b>.</li>
      <li>Потому что в учебном проекте с жёстким сроком главный результат — это <b>освоенные роли и процессы</b>.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Исходные условия</p>
    <h2 class="slideTitle">Задача и срок</h2>
    <ul>
      <li>Проект был сформулирован так: <b>«Определение качества бутилированной воды: состав, мутность и так далее»</b>.</li>
      <li>Срок выполнения — <b>1 день</b>.</li>
      <li>Мы — Анастасия Сергеевна и я. В команде, кроме коллеги, — <b>два ИИ-ассистента разработки</b>.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Ключевое решение</p>
    <h2 class="slideTitle">Максимум пользы для обучения</h2>
    <ul>
      <li>За 1 день нельзя качественно выполнить реальный проект — поэтому мы не имитировали «почти прод».</li>
      <li>Вместо этого построили работу так, чтобы получить <b>максимальную пользу для собственного обучения</b>.</li>
      <li><b>Анастасия Сергеевна</b> — освоить новую область ИТ-технологий.</li>
      <li><b>Я</b> — освоить роль <b>руководителя коллектива разработчиков</b>.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Команда и инструменты</p>
    <h2 class="slideTitle">Кто и чем работал</h2>
    <div class="cols">
      <div class="card"><h3>Ведущий (я)</h3><p>Модель <b>DeepSeek</b> — оптимум цена/качество, под управлением ИИ-ассистента <b>Kilo Code</b>.</p></div>
      <div class="card"><h3>Коллега</h3><p>Модель <b>GLM</b> — высокоэффективная и дорогая, под управлением ИИ-ассистента <b>Claude Code</b>.</p></div>
    </div>
    <ul style="margin-top:16px"><li>Разная цена и разная сила моделей — сознательно использованы как инструмент: <b>дешёвая делает объём, сильная проверяет</b>.</li></ul>'''))

slides.append(slide('''    <p class="eyebrow">Поиск ниши</p>
    <h2 class="slideTitle">Надстройка, а не слом технологии</h2>
    <ul>
      <li>Производство бутилированной воды — <b>отлаженный процесс</b>; проверка качества уже заложена в стандартные технологические решения.</li>
      <li>Ломать действующие процессы бессмысленно — мы искали <b>свою нишу</b>.</li>
      <li>Цель: <b>надстройка над существующей системой контроля качества</b>, закрывающая её недостатки.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Проблема</p>
    <h2 class="slideTitle">Реактивный контроль → предиктивный</h2>
    <ul>
      <li>Существующая система <b>только отбраковывает</b> партию — уже произведённую.</li>
      <li>Нужен <b>предиктивный</b> контроль: раннее предупреждение о риске.</li>
      <li>Предположение: на многих предприятиях процесс <b>ручной</b> → человеческий фактор, запаздывание реакции, отсутствие объективной истории, разрозненность данных, неповторяемость практик, сложность аудита.</li>
      <li>Берём преимущества ИИ, но видим и <b>проблемы внедрения</b>: стохастичность, FP/FN, эффект автоматизации, ответственность, разметка данных, дрейф, ИБ.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Организация работы</p>
    <h2 class="slideTitle">Моделировали реальный процесс</h2>
    <ul>
      <li>Не делили проект на полностью <b>независимые модули</b>.</li>
      <li>Разделили ответственность по принципу:
        <ul style="margin-top:8px">
          <li>равноценности вклада каждого участника;</li>
          <li>максимальной пользы от участия для каждого;</li>
          <li>учёта сильных сторон каждого, <b>включая ИИ-модели</b>.</li>
        </ul>
      </li>
    </ul>
    <p class="sub" style="margin-top:14px">Сознательно пошли на связанность задач и совместную работу над одними артефактами — потому что именно конфликты и есть <b>реальность</b>, а не учебная модель.</p>'''))

slides.append(slide('''    <p class="eyebrow">Роли</p>
    <h2 class="slideTitle">Распределение ответственности</h2>
    <div class="cols">
      <div class="card"><h3>Ведущий (я)</h3><p>Руководство проектом, концепция, планирование и текущее управление, черновые артефакты СА (кроме ФТ), бэклог, бэкенд (по факту не дошло), вопросы ИИ.</p></div>
      <div class="card"><h3>Анастасия Сергеевна</h3><p>Функциональные требования, все диаграммы, образцы экранных форм, презентация Заказчику, чистовая доработка Договора.</p></div>
    </div>
    <ul style="margin-top:16px"><li>ИИ-помощник коллеги — <b>роль судьи</b>: технология <b>«LLM-as-a-Judge»</b> (сильная модель критикует результаты дешёвой).</li></ul>'''))

slides.append(slide('''    <p class="eyebrow">Результат за сутки</p>
    <h2 class="slideTitle">Что получилось</h2>
    <ul>
      <li><b>Проект Договора</b> на выполнение работ.</li>
      <li><b>Техническое задание (ТЗ)</b>.</li>
      <li><b>Образцы экранных форм</b> — для представления Заказчику.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Главная трудность</p>
    <h2 class="slideTitle">Границы проекта (Vision and Scope)</h2>
    <ul>
      <li>Труднее всего — на первом этапе: чётко <b>разграничить зону ответственности</b> проекта от остальной существующей технологической цепочки.</li>
      <li>Здесь очень помогла техника <b>«LLM-as-a-Judge»</b>: сильная модель выявляла <b>неточности формулировок</b>.</li>
      <li>Неточность формулировки на раннем этапе → <b>галлюцинации</b> моделей на поздних этапах.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Планирование</p>
    <h2 class="slideTitle">Пошагово, с перепроверкой</h2>
    <ul>
      <li>Отказались от соблазна поручить ИИ «сделать всё и сразу».</li>
      <li>Каждый шаг, выполненный <b>дешёвой</b> моделью, <b>перепроверялся сильной</b> моделью.</li>
      <li>Планирование и пошаговое выполнение — не формальность, а способ удержать качество.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Особый случай</p>
    <h2 class="slideTitle">ИИ-модели вступили в прямой контакт</h2>
    <ul>
      <li>Неожиданно обнаружили: <b>две ИИ-модели сами установили контакт</b> между собой.</li>
      <li>Они создали в репозитории проекта <b>папку</b> и помещали туда сообщения друг другу.</li>
      <li>Я заметил это, когда моя модель «проговорилась», что ей надо ответить на адресованное ей сообщение.</li>
      <li>Я попросил показать диалог и <b>взял его под свой контроль</b>: стал поручать своей модели давать сильной модели прямые указания по <b>предотвращению конфликтов</b> при совместной работе над артефактами.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Артефакт · глоссарий</p>
    <h2 class="slideTitle">Glossary — словарь смыслов</h2>
    <ul>
      <li>Особое внимание — артефакту <b>glossary</b>: он <b>постоянно пополнялся</b>.</li>
      <li>Следили, чтобы во всех артефактах использовались <b>одни и те же термины</b>.</li>
      <li>Периодически моделям ставилась задача <b>проверять полноту словаря</b> — чтобы не оставалось непонятных или неоднозначных терминов и сокращений.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Пример из практики</p>
    <h2 class="slideTitle">Аббревиатура «КА»</h2>
    <ul>
      <li>Корректирующее действие обозначается префиксом <code>CA</code> (corrective action).</li>
      <li>Одна из моделей по аналогии предложила русское сокращение <b>«КА»</b> — это порождало неоднозначность.</li>
      <li>В глоссарий внесли явный запрет: <b>«корректирующее действие (в идентификаторах — префикс CA; аббревиатура "КА" не используется)»</b>.</li>
      <li>Так глоссарий стал <b>инструментом против галлюцинаций</b>, а не формальным приложением.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Артефакт · references</p>
    <h2 class="slideTitle">Папка вспомогательных материалов</h2>
    <ul>
      <li>Папка <b>references</b> — хранилище материалов, найденных в интернете или полученных в ИИ-чатах.</li>
      <li>Назначение — помочь команде <b>глубже понимать задачу</b>.</li>
      <li>Пример: обзор подходов к <b>поиску аномалий</b> в данных (алгоритмы, оконные признаки, residual/reconstruction).</li>
      <li>Экономит время: вместо повторного поиска опираемся на уже собранную и проверенную базу.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Выводы</p>
    <h2 class="slideTitle">Что мы вынесли</h2>
    <ul>
      <li>В учебном проекте главное — <b>освоенные роли и процессы</b>, а не «почти готовый продукт».</li>
      <li>Разделение по сильным сторонам + перекрёстная проверка <b>«дешёвая делает — сильная проверяет»</b> → управляемое качество.</li>
      <li>Дисциплина артефактов (<b>Vision and Scope, глоссарий, references</b>) защищает от галлюцинаций и масштабирует команду «человек + ИИ».</li>
      <li>Связанность задач и реальные конфликты — это <b>процесс, переносимый на реальные проекты</b>.</li>
    </ul>'''))

slides.append(slide('''    <p class="eyebrow">Материалы проекта</p>
    <h2 class="slideTitle">Экраны интерфейса — SCR-01…SCR-12</h2>
    <p class="sub">Далее — макеты всех экранных форм, затем полный текст Договора и ТЗ (с прокруткой) и презентация для Заказчика.</p>'''))

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

slides.append(slide(
    '    <p class="eyebrow">Документы · для Заказчика</p>'
    '<h2 class="slideTitle">Презентация для Заказчика</h2>'
    '<p class="docScrollHint">Одностраничная презентация (прокрутите её внутри окна).</p>'
    '<iframe class="frame" style="height:74vh" src="system_analysis/presentation_customer.html" title="Презентация для Заказчика" loading="lazy"></iframe>'))

slides.append(slide('''    <p class="eyebrow">Итоги</p>
    <h2 class="slideTitle">Спасибо! Вопросы?</h2>
    <ul>
      <li>Говорили о <b>процессе</b>: команда «человек + ИИ», роли, перекрёстная проверка, глоссарий, references.</li>
      <li>Полный текст Договора и ТЗ, все экранные формы и презентация Заказчику — в этой колоде.</li>
      <li>Исходный текст доклада — <code>docs/system_analysis/process_report.md</code>.</li>
    </ul>'''))

nav = '''
<div class="foot">AquaPredict · процесс разработки · 2026 · <a href="https://github.com/igorvolk1961/water_checker">репозиторий</a></div>
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
