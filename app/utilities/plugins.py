import zipfile
from os import listdir
from os.path import isfile, join
import yaml
import asyncio
from flask import current_app
from .util import Loggers


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
                plugin_name = plugin_yaml['name']
                plugin_version = plugin_yaml['version']
                plugins.append((plugin_name, plugin_version, jar_file))
        except Exception as e:
            Loggers.Error.error("Error in:"+ jar_file)
            Loggers.Error.error(e)
            pass
        plugins.sort()

    return plugins
