import re
import ssl
import time
import urllib.request
from pathlib import Path

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 9; MI 9)",
    "Referer": "http://dl.wenku8.com/",
}

BANNER = "轻小说文库"
DELAY = 2
RETRIES = 3


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        return resp.read()


def sanitize(name):
    return re.sub(r'[\\/:*?"<>|\r\n\t]', "_", name).strip(" .")


def crawl(book_id, save_dir):
    url = f"http://dl.wenku8.com/down.php?type=utf8&id={book_id}"
    for attempt in range(1, RETRIES + 1):
        try:
            text = fetch(url).decode("utf-8", "ignore")
            lines = text.splitlines()
            if BANNER not in lines[0] or len(lines) < 3:
                raise ValueError("invalid content")
            m = re.search(r"<(.+)>", "\n".join(lines[1:5]))
            title = sanitize(m.group(1)) if m else f"book_{book_id}"
            path = save_dir / f"{book_id}_{title}.txt"
            if path.exists():
                return path, "exists"
            path.write_text(text, encoding="utf-8", newline="")
            return path, "ok"
        except Exception as e:
            if attempt == RETRIES:
                return None, type(e).__name__
            time.sleep(DELAY * attempt)


def main():
    save_dir = Path(input("保存路径: ").strip().strip('"'))
    save_dir.mkdir(parents=True, exist_ok=True)
    raw = input("书籍ID(空格/逗号分隔): ").strip()
    ids = [i for i in re.split(r"[\s,，;；]+", raw) if i.isdigit()]
    if not ids:
        print("无有效ID")
        return
    done = 0
    for i, book_id in enumerate(ids, 1):
        path, status = crawl(book_id, save_dir)
        if path:
            size = path.stat().st_size / 1048576
            print(f"[{i}/{len(ids)}] {path.name} ({size:.2f} MB) {status}")
            done += 1
        else:
            print(f"[{i}/{len(ids)}] {book_id} 失败 {status}")
        if i < len(ids):
            time.sleep(DELAY)
    print(f"完成 {done}/{len(ids)}")


if __name__ == "__main__":
    main()
