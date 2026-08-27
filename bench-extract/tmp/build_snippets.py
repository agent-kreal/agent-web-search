#!/usr/bin/env python3
"""Собирает bench-extract/snippets.json — сниппет-золото для бенчмарка экстракторов."""
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parent.parent

DATA = {
    "article-en-1": [
        "the signal for key tokens to be amplified",
        "Google started using BERT to process search queries",
        "a chatbot based on a fine-tuned variant of GPT-3.5",
    ],
    "article-en-2": [
        "generate, summarize, translate, and analyze text in many contexts",
        "Substantial infrastructure is necessary for training the largest models",
        "might need more linguistic data than naturally available",
    ],
    "article-en-3": [
        "The following recipe assumes you're very ambitious",
        "you do when walking or taking a shower or lying in bed",
        "has to be interleaved with deliberate work that feeds it questions",
    ],
    "article-en-4": [
        "carved a deep bed shaded by trees and lined with blackberry bushes",
        "with an actual person tends to involve all the senses",
        "one measure of your own wealth, generosity and power",
    ],
    "article-en-5": [
        "Victor Pelevin made his name in 90s",
        "Deeply unpopular in France, President Macron relishes the international stage",
        "set about dismantling USAID, many around the world were shocked",
    ],
    "article-ru-1": [
        "Провайдера заблокировали без включения в реестр запрещённых сайтов",
        "блокировали с помощью ТСПУ — технических средств противодействия угрозам",
        "положительный исход дела поможет владельцам других ресурсов",
    ],
    "article-ru-2": [
        "трансформеры не требуют обработки последовательностей по порядку",
        "добавляет информацию о позиции каждого токена в последовательности",
        "позволяют модели легко интерполировать на более длинные последовательности",
    ],
    "article-ru-3": [
        "Собрал все нейросети 2026 года в одну таблицу",
        "Пишет живее ChatGPT, держит контекст в длинных диалогах",
        "Бесплатный видеоредактор с AI. Автосубтитры, удаление фона, нарезка",
    ],
    "article-ru-4": [
        "В Госдуме предложили формулировку определения искусственного интеллекта",
        "Разрабатываемый федеральный законопроект, как отмечает адвокат, не будет запрещающим",
        "Ключевое, на чем будут настаивать его авторы, — безопасность персональных данных",
    ],
    "docs-js-1": [
        "How to respond to events and update the screen",
        "count the number of times a button is clicked",
        "and the function that lets you update it",
    ],
    "docs-js-2": [
        "scanning all of your HTML files, JavaScript components",
        "start using Tailwind’s utility classes to style your content",
    ],
    "docs-js-3": [
        "have a content-addressable identifier called a digest",
        "We have four ways to set user memory usage",
        "as much memory and swap memory as they need",
    ],
    "docs-js-4": [
        "Create a new Next.js app and run it locally",
        "code editors can use for advanced type-checking and auto-completion",
        "save it to see the updated result in your browser",
    ],
    "docs-js-5": [
        "You are reading the documentation for Vue 3",
        "can grow with you and adapt to your needs",
        "is the recommended way to author Vue components",
    ],
    # HN: extraction почти целиком состоит из spacer-таблиц, осмысленного текста
    # в окнах head+mid мало — фразы взяты из того, что реально есть.
    "forum-1": [
        "My YC app: Dropbox - Throw away your USB drive",
        "on April 4, 2007",
        "71 comments",
    ],
    "forum-3": [
        "what is the best practice for spawning goroutine",
        "should pass the context in it and handle it there",
        "how a goroutine will stop, before you start it",
    ],
    "forum-4": [
        "В голосовании приняли участие 347 разработчиков",
        "И всё-таки, почему она Шрути, а не Срути?",
    ],
    "spa-app-1": [
        "Your drawings are saved in your browser's storage",
        "Save your work to a file regularly to avoid losing it",
    ],
    "spa-app-2": [
        "No Priority Low Priority Medium Priority High Priority Difficulty Adjustment",
        "Minimum fee Unconfirmed Memory Usage Incoming Transactions Recent Replacements",
    ],
    "spa-app-3": [
        "в Петербурге взорвался автомобиль с военным",
        "Флорист рассказала, какие букеты не стоит дарить учителю",
        "болезнь Альцгеймера не одинакова для разных наций",
    ],
    "spa-app-4": [
        "Photopea runs on your device, using your CPU and your GPU",
        "Our free online photo editor is a great tool for educational projects",
    ],
    "static-docs-1": [
        "This domain is for use in documentation examples without needing permission",
        "Avoid use in operations",
    ],
    "static-docs-2": [
        "provides a portable way of using operating system dependent functionality",
        "for objects representing a file system path",
        "Return the value of the environment variable",
    ],
    "static-docs-3": [
        "a stream of octets sent after the header section",
        "switch the connection to tunnel mode instead of having content",
        "when a complete or partial representation is transferred as message content",
    ],
    "static-docs-4": [
        "provides a high-level summary of changes to SQLite",
        "Enforce STRICT typing on computed columns",
        "Improved resistance to database corruption caused by an application",
    ],
    "tables-1": [
        "introduction to pandas, geared mainly for new users",
        "For getting fast access to a scalar",
        "where a boolean condition is met",
    ],
    "tables-2": [
        "SELECT, TABLE, WITH — retrieve rows from a table or view",
        "The seed value can be any non-null floating-point value",
        "as a result of clustering effects",
    ],
    "tables-3": [
        "The NumPy library contains multidimensional array data structures",
        "to preserve the indexing convention or not reorder the data",
        "insert an axis along the second dimension",
    ],
}


def main() -> int:
    out = {}
    for key, phrases in DATA.items():
        md = BENCH / "tmp-full" / f"{key}.md"
        boi = BENCH / "tmp-full" / f"{key}.boiler.json"
        without = json.loads(boi.read_text())
        out[key] = {"with": phrases, "without": without}
    dest = BENCH / "snippets.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"{dest}: {len(out)} ключей, "
          f"{sum(len(v['with']) for v in out.values())} with-фраз, "
          f"{sum(len(v['without']) for v in out.values())} without-фраз")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
