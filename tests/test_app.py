from fastapi import fastAPI 
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', repsonse_class=HTMLRepsonses)
def read_root():
    return """
    <html>
        <head>
            <title> Nosso olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
    </html>"""