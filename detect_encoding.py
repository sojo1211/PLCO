import subprocess

res = subprocess.run(['git', 'show', 'HEAD:match_intelligence/frontend/src/components/MatchDetail.jsx'], capture_output=True)
raw_bytes = res.stdout

for enc in ['utf-8', 'cp949', 'euc-kr', 'utf-16']:
    try:
        text = raw_bytes.decode(enc)
        print(f"Success with {enc}: {len(text)} chars, lines: {len(text.splitlines())}")
        # print first few characters
        print(text[:100])
        break
    except Exception as e:
        print(f"Failed with {enc}: {e}")
