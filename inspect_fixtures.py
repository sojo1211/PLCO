content = open('match_intelligence/api_server.py', 'r', encoding='utf-8').read()
idx = content.find("def fixtures():")
if idx != -1:
    print(content[idx:idx+800])
else:
    print("fixtures() not found")
