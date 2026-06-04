import os

brain_dir = r"C:\Users\sungj\.gemini\antigravity\brain"
for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file == "overview.txt":
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if "MatchDetail.jsx" in line:
                            # Print the line if it is from a previous conversation (exclude current)
                            if "27821a74" not in path:
                                print(f"From {os.path.basename(os.path.dirname(os.path.dirname(root)))}: {line[:200].strip()}")
            except Exception as e:
                pass
