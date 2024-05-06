from loguru import logger
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

def check_token(token):
    logger.info(f"Проверяем токен - {token}")

    command = f'curl -s -H "Authorization: {token}" https://discord.com/api/v9/users/@me'

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    if process.returncode == 0:
        return token, json.loads(output.decode("utf-8"))
    else:
        return token, {"message": "401: Unauthorized", "code": 0}

goods_file = open("goods.txt", "w", encoding="utf-8")
bads_file = open("bads.txt", "w", encoding="utf-8")

with open('tokens.txt', 'r') as file:
    tokens = file.readlines()
    tokens = [token.strip() for token in tokens]

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_token, token) for token in tokens]

    for future in futures:
        token, result = future.result()
        if "message" in result:
            bads_file.write(f"Токен: {token}\n")
            bads_file.write(json.dumps(result, indent=4))
            bads_file.write("\n\n")
        else:
            goods_file.write(f"Токен: {token}\n")
            goods_file.write(json.dumps(result, indent=4))
            goods_file.write("\n\n")

goods_file.close()
bads_file.close()