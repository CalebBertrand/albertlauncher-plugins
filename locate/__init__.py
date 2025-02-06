# -*- coding: utf-8 -*-
# Copyright (c) 2022-2024 Manuel Schneider

"""
Patched version of the original locate plugin, this one uses plocate instead
"""


import shlex
import subprocess
from pathlib import Path

from albert import *

md_iid = '2.3'
md_version = "1.10"
md_name = "Locate"
md_description = "Find and open files using locate"
md_license = "MIT"
md_url = "https://github.com/albertlauncher/python/tree/main/locate"
md_bin_dependencies = "locate"
md_authors = "@manuelschneid3r"
locate_command = "plocate"


class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self, self.id, self.name, self.description,
            synopsis='<locate params>',
            defaultTrigger="'"
        )

        self.iconUrls = [
            "xdg:preferences-system-search",
            "xdg:system-search",
            "xdg:search",
            "xdg:text-x-generic",
            f"file:{Path(__file__).parent}/locate.svg"
        ]

    def handleTriggerQuery(self, query):
        if len(query.string) > 2:

            try:
                args = shlex.split(query.string)
            except ValueError:
                return

            result = subprocess.run([locate_command, *args], stdout=subprocess.PIPE, text=True)
            if not query.isValid:
                return
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
                            Action("open", "Open", lambda p=path: runTerminal("nvim %s" % p))
                        ]
                    )
                )
