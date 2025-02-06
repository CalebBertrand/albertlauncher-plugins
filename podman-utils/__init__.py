# -*- coding: utf-8 -*-
# Copyright (c) 2022-2024 Manuel Schneider

"""
An albert launcher plugin for working with running podman containers
"""


import subprocess
from pathlib import Path

from albert import *

md_iid = '2.4'
md_version = "1.0"
md_name = "Podman Utils"
md_description = "View and do simple operations on currently running podman containers"
md_license = "MIT"
md_bin_dependencies = "fzf"
md_url = "https://github.com/CalebBertrand"
md_authors = "Caleb Bertrand"


class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
                self, self.id, self.name, self.description,
                synopsis='<[s]tart|[k]ill|[l]ogs|[r]estart>',
                defaultTrigger="pod"
                )

        self.iconUrls = [f"file:{Path(__file__).parent}/docker.png"]

    def runDetachedScript(self, script):
        runDetachedProcess(['sh', '-c', script])

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return

        command = ['sh', '-c', 'podman container list -a --noheading --format "{{.ID}}|{{.Names}}|{{.Status}}"']
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        lines = sorted(result.stdout.splitlines(), reverse=True)

        if not query.isValid:
            return

        def handleAction(id=None):
            if not query.isValid or not id:
                return

            input_command = query.string.strip()
            
            if input_command.startswith('s'):
                self.runDetachedScript(script='podman container start {}'.format(id))

            if input_command.startswith('l'):
                self.runDetachedScript(script='podman container logs -f {}'.format(id))

            if input_command.startswith('k'):
                self.runDetachedScript(script='podman container kill {}'.format(id))

            if input_command.startswith('r'):
                self.runDetachedScript(script='podman container restart {}'.format(id))

        for line in lines:
            id, name, status = line.split('|')
            query.add(
                    StandardItem(
                        id=name,
                        text=name,
                        subtext=status,
                        iconUrls=self.iconUrls,
                        actions=[Action("open", "Open", lambda x=id: handleAction(x))]
                        )
                    )

