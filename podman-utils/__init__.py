"""
An albert launcher plugin for working with podman containers
"""


import subprocess
from pathlib import Path
from time import sleep

from albert import *

md_iid = '3.0'
md_version = "1.0"
md_name = "Podman Utils"
md_description = "View and do simple operations on podman containers"
md_license = "MIT"
md_bin_dependencies = "fzf"
md_url = "https://github.com/CalebBertrand"
md_authors = "Caleb Bertrand"


class Plugin(PluginInstance, TriggerQueryHandler):

    iconUrls = [f"file:{Path(__file__).parent}/docker.png"]

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(self)


    def synopsis(self, query):
        return '<[s]tart|[k]ill|[l]ogs|[r]estart>'

    def defaultTrigger(self):
        return 'pod '

    def runDetachedScript(self, script):
        runDetachedProcess(['sh', '-c', script])

    def handleTriggerQuery(self, query):
        if not query.isValid:
            return

        command = ['sh', '-c', 'podman container list -a --noheading --format "{{.ID}}|{{.Names}}|{{.Status}}"']
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
        proc.wait()

        rawtext = proc.stdout.read()
        rawLines = filter(lambda x: len(x) > 0, rawtext.split('\n'))
        sortedLines = sorted(rawLines, reverse=True)

        if not query.isValid:
            return

        def handleAction(id=None):
            if not query.isValid or not id:
                return

            input_command = query.string.strip()

            if input_command.startswith('s'):
                self.runDetachedScript(script='podman container start {}'.format(id))
            elif input_command.startswith('l'):
                self.runDetachedScript(script='podman container logs -f {}'.format(id))
            elif input_command.startswith('k'):
                self.runDetachedScript(script='podman container kill {}'.format(id))
            elif input_command.startswith('r'):
                self.runDetachedScript(script='podman container restart {}'.format(id))

        items = []
        for line in sortedLines:
            id, name, status = line.split('|')
            items.append(
                    StandardItem(
                        id=name,
                        text=name,
                        subtext=status,
                        iconUrls=self.iconUrls,
                        actions=[Action("open", "Open", lambda x=id: handleAction(x))]
                        )
                    )

        query.add(items)

