import re

def extract_plain_text(vtt_file_path):
    with open(vtt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    spoken_lines = []
    for line in lines:
        if re.match(r'\d\d:\d\d:\d\d\.\d+ -->', line):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'align:start.*', '', line)
        line = line.strip()
        if line:
            spoken_lines.append(line)

    cleaned = []
    [cleaned.append(l) for l in spoken_lines if l not in cleaned]

    return '\n'.join(cleaned)
