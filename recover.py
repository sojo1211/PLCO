import os
import re
import json

brain_dir = r"C:\Users\sungj\.gemini\antigravity\brain"
output_dir = r"c:\Users\sungj\OneDrive\Desktop\플코 진\match_intelligence"

print("Starting recovery search in brain directory...")
found_any = False

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
                print(f"Found MatchDetail.jsx reference in {path}")
                # We search for json strings containing CodeContent or simply the file content of MatchDetail
                # The log might have JSON payloads. Let's search for "CodeContent":"..." or similar patterns
                # Let's search for matches starting with "import { useState" and ending with "export default function MatchDetail" or similar
                # Let's extract the longest block that looks like React code for MatchDetail
                matches = re.findall(r'("CodeContent"\s*:\s*".*?"|CodeContent\s*=\s*".*?")', content, re.DOTALL)
                print(f"Found {len(matches)} raw matches.")
                
                # Let's also do a search directly for blocks of React code
                # The React code starts with `import { useState, useEffect } from 'react'` and ends with the component render/export
                react_blocks = re.findall(r"(import\s+\{\s*useState\s*,\s*useEffect\s*\}\s+from\s+['\"]react['\"].*?export\s+default\s+function\s+MatchDetail\b.*?<\/div>\s*\)\s*\r?\n\s*\})", content, re.DOTALL)
                print(f"Found {len(react_blocks)} react block matches.")
                
                for idx, block in enumerate(react_blocks):
                    # Check if it has YOLOv11 and images
                    if "YOLOv11" in block and "tactical_analysis_dashboard.png" in block:
                        print(f"React block {idx} is a candidate!")
                        out_path = os.path.join(output_dir, f"MatchDetail_recovered_block_{idx}.jsx")
                        with open(out_path, "w", encoding="utf-8") as out_f:
                            out_f.write(block)
                        print(f"Saved candidate React block to {out_path}")
                        found_any = True
                        
                # Let's also parse JSON if there are any JSON strings in the log
                # We can find all JSON blocks in the log and parse them to find the original file write
                json_blocks = re.findall(r"(\{.*?\})", content, re.DOTALL)
                for j_idx, j_str in enumerate(json_blocks):
                    if "MatchDetail.jsx" in j_str and ("CodeContent" in j_str or "ReplacementContent" in j_str):
                        try:
                            # Try parsing as JSON
                            parsed = json.loads(j_str)
                            content_val = parsed.get("CodeContent") or parsed.get("ReplacementContent")
                            if content_val and "EVENT_ICON" in content_val and "YOLOv11" in content_val:
                                print(f"Found valid JSON block with content!")
                                out_path = os.path.join(output_dir, f"MatchDetail_recovered_json_{j_idx}.jsx")
                                with open(out_path, "w", encoding="utf-8") as out_f:
                                    out_f.write(content_val)
                                print(f"Saved recovered JSON content to {out_path}")
                                found_any = True
                        except Exception:
                            # Not a valid JSON or some parsing error, ignore
                            pass

if not found_any:
    print("No clean MatchDetail.jsx found in logs. We might need to look deeper into file changes or git reflog.")
else:
    print("Recovery run completed successfully!")
