from starlette.templating import Jinja2Templates

from core.settings import ROOT_DIR

templates = Jinja2Templates(directory=ROOT_DIR / "src/static/html")
