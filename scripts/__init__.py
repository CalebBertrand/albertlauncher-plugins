# -*- coding: utf-8 -*-
# Copyright (c) 2022-2024 Manuel Schneider

"""
A albert plugin which will allow you to run scripts under a specified folder
"""


import subprocess
from pathlib import Path
import os

from albert import *

md_iid = '2.4'
md_version = "1.0"
md_name = "Run Scripts"
md_description = "Run scripts from your specified folder"
md_license = "MIT"
md_bin_dependencies = "fzf"
md_url = "https://github.com/CalebBertrand"
md_authors = "Caleb Bertrand"

class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
                self, self.id, self.name, self.description,
                synopsis='<script name>',
                defaultTrigger=">"
                )

        self.iconUrls = [f"file:{Path(__file__).parent}/terminal.png"]

        home_dir = os.environ['HOME']
        self.scripts_dir = home_dir + '/scripts'

        

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return
        if len(query.string) > 1:
            command = ['sh', '-c', 'ls {scripts_dir} | fzf --filter="{query}"'.format(scripts_dir=self.scripts_dir, query=query.string)]
        else:
            command = ['ls', self.scripts_dir]

        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        lines = [x for x in sorted(result.stdout.splitlines(), reverse=True) if x.endswith('.sh')]

        if not query.isValid:
            return

        for path in lines:
            name = Path(path).name.split('.')[0]
            query.add(
                    StandardItem(
                        id=path,
                        text=name,
                        iconUrls=[self.scripts_dir + '/' + name + '.png'] + self.iconUrls,
                        actions=[
                            Action("open", "Open", lambda p=path: runDetachedProcess(['sh', self.scripts_dir + '/' + p]))
                            ]
                        )
                    )
