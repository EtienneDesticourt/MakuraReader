
def escape(text):
    escaped_data = ""
    for c in text:
        escaped_data += "&#" + hex(ord(c))[1:]
    # escaped_data = escaped_data.replace("&#xa&", "<br>&")
    return escaped_data


def generate_page_html(tokens, furigana=False, translation=False):
    html = "<p>"
    for i, token in enumerate(tokens):
        if furigana:
            if token.has_kanji():
                kanji_head, furi_head, kana_tail = token.strip()
                token_html = "<ruby>%s<rt>%s</rt></ruby>%s" % (escape(kanji_head), escape(furi_head), escape(kana_tail))
            else:
                token_html = escape(token.raw)
        elif translation:
            if token.translation != "":
                token_html = "<ruby>%s<rt class='translation'>%s</rt></ruby>" % (escape(token.raw), token.translation)
            else:
                token_html = escape(token.raw)
        else:
            token_html = escape(token.raw)

        html += "<span class='token' onclick='load_token_definition(%s);return false;'>%s</span>" % (i, token_html)
    html += "</p>"
    with open("temptemp.txt", "w", encoding="utf8") as f:
        f.write(html)
    return html


def generate_token_definition_html(token):
    html = ""

    word = "<h1 class='word'>" + escape(token.base) + "</h1>"
    hiragana = "<h3 class='hiragana'>" + escape(token.furigana) + "</h3>"
    try:
        definition = "<p class='text'>" + token.translation + "</p>"
    except IndexError:
        definition = "<p class='text'></p>"

    html += word + "<br>" + hiragana + "<br>" + definition
    print(html)
    return html
