

import shutil
from firefly.html.components.toc import TableofContent
from firefly.html.fake_report import create_fake_report
from bs4 import BeautifulSoup
from pathlib import Path

working_dir = Path("work/temp")

if working_dir.exists():
    shutil.rmtree(working_dir)

a=create_fake_report(working_dir / "fake_report.html")

toc = TableofContent(content=a.get_html())

new_html = toc.render()

# write the new html to a file
with open(working_dir / "fake_report_with_toc.html", "w",encoding="utf-8") as file:
    file.write(new_html)


