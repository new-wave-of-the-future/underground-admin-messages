import urllib.request
import re
from html.parser import HTMLParser


class CleanFullParser(HTMLParser):
    def __init__(self, target_id):
        super().__init__()
        self.target_id = target_id
        self.recording = False
        self.nesting_level = 0
        self.captured_html = []
        # Tags we usually want to ignore inside an announcement
        self.ignore_tags = {"script", "style", "meta"}
        self.current_tag_ignored = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if attrs_dict.get("id") == self.target_id:
            self.recording = True
            self.nesting_level = 1
            return

        if self.recording:
            self.nesting_level += 1
            if tag in self.ignore_tags:
                self.current_tag_ignored = True
                return

            attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
            self.captured_html.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        if self.recording:
            self.nesting_level -= 1
            if self.nesting_level == 0:
                self.recording = False
            elif tag in self.ignore_tags:
                self.current_tag_ignored = False
            else:
                self.captured_html.append(f"</{tag}>")

    def handle_data(self, data):
        if self.recording and not self.current_tag_ignored:
            # Clean up excessive whitespace/newlines within the text
            clean_data = re.sub(r"\s+", " ", data)
            if clean_data.strip():
                self.captured_html.append(clean_data)

    def get_content(self):
        raw_html = "".join(self.captured_html).strip()
        # Final pass: remove empty lines and fix spacing between tags
        return re.sub(r">\s+<", "><", raw_html)


def scrape_and_clean(url):
    try:
        # Headers help avoid 403 Forbidden errors
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode("utf-8")

        parser = CleanFullParser("announce")
        parser.feed(html_content)
        return parser.get_content()
    except Exception as e:
        return f"Error: {e}"


# Usage
final_html = scrape_and_clean("https://underground.boardhost.com/index.php")
print(final_html)
