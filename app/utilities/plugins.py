import zipfile
from os import listdir
from os.path import isfile, join
import yaml
import asyncio
from flask import current_app


async def get_plugins():
    plugins = []
    plugin_path = current_app.config['MINECRAFT_PLUGIN_FOLDER']

    plugin_files = [f for f in listdir(
        plugin_path) if isfile(join(plugin_path, f))]

    for jar_file in plugin_files:
        try:
            f = zipfile.ZipFile(join(plugin_path,jar_file), 'r')
            if 'plugin.yml' in f.namelist():
                plugin_file = f.open('plugin.yml', 'r')
                plugin_yaml = yaml.load(plugin_file, Loader=yaml.FullLoader)
                print(plugin_yaml)
                plugin_name = plugin_yaml['name']
                plugins.append((plugin_name, jar_file))
        except Exception as e:
            print(e)
        plugins.sort()

    return plugins
