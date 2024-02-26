

import re
import shutil
from firefly.html.fake_report import create_fake_report
from pathlib import Path

working_dir = Path("work/temp")

if working_dir.exists():
    shutil.rmtree(working_dir)

a=create_fake_report(working_dir / "fake_report.html")

from firefly.html.toc import Toc

tt = Toc(html_in=a.get_html())

tt.make_toc()

print(tt.html_toc)

from bs4 import BeautifulSoup
from pathlib import Path

Soup = BeautifulSoup(a.get_html(), 'html.parser')

heading_tags = ["h1", "h2", "h3"]
for tags in Soup.find_all(heading_tags):
    print(tags.name + ' -> ' + tags.text.strip())
    print(tags.get('id'))