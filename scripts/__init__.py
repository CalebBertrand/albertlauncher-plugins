# -*- coding: utf-8 -*-
# Copyright (c) 2022-2024 Manuel Schneider

"""
A albert plugin which will allow you to run scripts under a specified folder
"""


import shlex
import subprocess
from pathlib import Path

from albert import *

md_iid = '2.4'
md_version = "1.0"
md_name = "Run Scripts"
md_description = "Run scripts from your specified folder"
md_license = "MIT"
md_bin_dependencies = "fzf"
md_url = "https://github.com/CalebBertrand"
md_authors = "Caleb Bertrand"

scripts_dir = '/home/caleb/scripts'

class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
                self, self.id, self.name, self.description,
                synopsis='<script name>',
                defaultTrigger=">"
                )

        self.iconUrls = [f"file:{Path(__file__).parent}/terminal.png"]

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return
# 'ls {scripts_dir} | fzf --filter={query}'.format(scripts_dir=scripts_dir, query=query.string) if len(query.string) > 1 else 
        command = 'ls {scripts_dir}'.format(scripts_dir=scripts_dir)
        result = subprocess.run(command.split(' '), stdout=subprocess.PIPE, text=True)
        lines = sorted(result.stdout.splitlines(), reverse=True)

        if not query.isValid:
            return

        for path in lines:
            query.add(
                    StandardItem(
                        id=path,
                        text=Path(path).name,
                        subtext=path,
                        iconUrls=self.iconUrls,
                        actions=[
                            Action("open", "Open", lambda p=path: runDetachedProcess(['sh', scripts_dir + '/' + p]))
                            ]
                        )
                    )

