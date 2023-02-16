from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    content = """
    <html>
        <head>
            <title>WebSocket Test</title>
        </head>
        <body>
            <h1>WebSocket Test</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id="messages"></ul>
            <script>
                var socket = new WebSocket("ws://localhost:8000/ws");
                socket.onmessage = function(e) {
                    var messages = document.getElementById("messages");
                    var message = document.createElement("li");
                    message.innerHTML = e.data;
                    messages.appendChild(message);
                };
                function sendMessage(event) {
                    event.preventDefault();
                    var input = document.getElementById("messageText");
                    console.log(input.value);
                    socket.send(input.value);
                    input.value = "";
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
        # check if websocket is closed
        except WebSocketDisconnect:
            break