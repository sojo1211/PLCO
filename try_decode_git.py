import subprocess

try:
    # Get raw bytes of the file from git commit 49ab1da
    cmd = ["git", "show", "49ab1da:match_intelligence/frontend/src/components/MatchDetail.jsx"]
    raw_bytes = subprocess.check_output(cmd)
    
    # Try decoding with cp949/euc-kr
    encodings = ['cp949', 'euc-kr', 'utf-8', 'latin1']
    for enc in encodings:
        try:
            text = raw_bytes.decode(enc)
            # Count the occurrences of Korean characters
            korean_chars = len([c for c in text if '\uac00' <= c <= '\ud7a3'])
            question_marks = text.count('?')
            print(f"Encoding '{enc}': {korean_chars} Korean characters, {question_marks} question marks")
            # Print sample lines from getEventDescription (lines 8-30)
            lines = text.splitlines()
            if len(lines) > 20:
                print("  Sample lines (8-16):")
                for i in range(7, 16):
                    print(f"    {i+1}: {lines[i]}")
        except Exception as e:
            print(f"Encoding '{enc}' failed: {e}")
            
except Exception as e:
    print("Error running git:", e)
