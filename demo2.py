

import shutil
from firefly.html.fake_report import create_fake_report
from pathlib import Path

working_dir = Path("work/temp")

if working_dir.exists():
    shutil.rmtree(working_dir)
    
create_fake_report(working_dir / "fake_report.html")
