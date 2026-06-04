import os
import re

brain_dir = r"C:\Users\sungj\.gemini\antigravity\brain"
output_dir = r"c:\Users\sungj\OneDrive\Desktop\플코 진\match_intelligence"

print("Starting raw regex search in brain logs...")
found_count = 0

# We search for something like:
# "import { useState" ... "export default function MatchDetail" ...
# but let's just search for any block that starts with import and has "MatchDetail" and "YOLOv11" in it.

for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if file == "overview.txt":
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {path}: {e}")
                continue
            
            if "MatchDetail.jsx" in content:
                print(f"Found MatchDetail.jsx reference in: {path}")
                
                # Let's search for any multi-line blocks starting with import and containing MatchDetail
                # Let's search for code blocks inside Markdown: ```jsx ... ``` or ```javascript ... ```
                code_blocks = re.findall(r"```(?:jsx|javascript|js|)\n(import\s+\{\s*useState.*?)\n```", content, re.DOTALL)
                print(f"  Found {len(code_blocks)} markdown code blocks starting with import.")
                
                for idx, block in enumerate(code_blocks):
                    if "MatchDetail" in block and "YOLOv11" in block:
                        out_name = f"recovered_md_block_{idx}_{len(block)}.jsx"
                        out_path = os.path.join(output_dir, out_name)
                        with open(out_path, "w", encoding="utf-8") as out_f:
                            out_f.write(block)
                        print(f"    -> Saved block of length {len(block)} to {out_name}")
                        found_count += 1
                
                # Also check JSON escaped strings: "CodeContent": "import ... "
                # We can find strings starting with "import {\n  useState" and ending with "}"
                # Let's do a simple regex for escaped code content
                escaped_blocks = re.findall(r"\"(?:CodeContent|ReplacementContent)\"\s*:\s*\"(import\s+.*?)\"", content, re.DOTALL)
                print(f"  Found {len(escaped_blocks)} JSON-escaped blocks.")
                for idx, block in enumerate(escaped_blocks):
                    # Replace escaped newlines
                    block_unesc = block.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"').replace("\\\\", "\\")
                    if "MatchDetail" in block_unesc and "YOLOv11" in block_unesc:
                        out_name = f"recovered_json_block_{idx}_{len(block_unesc)}.jsx"
                        out_path = os.path.join(output_dir, out_name)
                        with open(out_path, "w", encoding="utf-8") as out_f:
                            out_f.write(block_unesc)
                        print(f"    -> Saved JSON-escaped block of length {len(block_unesc)} to {out_name}")
                        found_count += 1

print(f"Done. Found {found_count} blocks.")
