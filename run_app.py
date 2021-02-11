from webui import WebUI
from VicSM import create_app

app = create_app()
ui = WebUI(app, debug=True)
ui.view.page().profile().clearHttpCache()
ui.run()