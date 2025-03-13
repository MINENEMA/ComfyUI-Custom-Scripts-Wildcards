from server import PromptServer
from aiohttp import web
import os
import folder_paths

wildcard_dir = os.path.abspath(os.path.join(__file__, "../../../comfyui-impact-pack/wildcards"))
user_dir = os.path.abspath(os.path.join(__file__, "../../user"))
autocomplete_file = os.path.join(user_dir, "autocomplete.txt")

if not os.path.exists(wildcard_dir):
    os.makedirs(wildcard_dir)
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

def get_wildcard_files():
    wildcard_files = []
    for root, _, files in os.walk(wildcard_dir):
        for file in files:
            if file.endswith('.txt'):
                wildcard_files.append(os.path.join(root, file))
    return wildcard_files

@PromptServer.instance.routes.get("/pysssss/autocomplete")
async def get_autocomplete(request):
    if os.path.isfile(autocomplete_file):
        return web.FileResponse(autocomplete_file)
    return web.Response(status=404)

@PromptServer.instance.routes.post("/pysssss/autocomplete")
async def update_autocomplete(request):
    with open(autocomplete_file, "w", encoding="utf-8") as f:
        f.write(await request.text())
    return web.Response(status=200)

@PromptServer.instance.routes.get("/pysssss/loras")
async def get_loras(request):
    loras = folder_paths.get_filename_list("loras")
    return web.json_response(list(map(lambda a: os.path.splitext(a)[0], loras)))

@PromptServer.instance.routes.get("/pysssss/wildcards")
async def get_wildcards(request):
    wildcard_data = {}
    for filepath in get_wildcard_files():
        filename = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, 'r', encoding='utf-8') as f:
            wildcard_data[filename] = [line.strip() for line in f if line.strip()]
    return web.json_response(wildcard_data)
