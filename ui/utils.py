
def escape(text):
    escaped_data = ""
    for c in text:
        escaped_data += "&#" + hex(ord(c))[1:]
    # escaped_data = escaped_data.replace("&#xa&", "<br>&")
    return escaped_data


def generate_page_html(tokens, furigana=False, translation=False):
    html = "<p>"
    for token in tokens:
        if furigana:
            token_html = "<ruby>%s<rt>%s</rt></ruby>" % (escape(token.raw), escape(token.kana))
        elif translation:
            token_html = "<ruby>%s<rt>%s</rt></ruby>" % (escape(token.raw), escape(token.english))
        else:
            token_html = escape(token.raw)

        html += token_html
    html += "</p>"
    with open("temptemp.txt", "w", encoding="utf8") as f:
        f.write(html)
    return html


def generate_token_definition_html(token):
    return ""
