from typing import Dict, Any
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import database_helper

app = FastAPI()

@app.get("/getstudents")
async def getstudents():
    return database_helper.students()

@app.post("/insert/")
async def insert(firstname: str, lastname: str, email: str, number_of_tickets: int, number_of_hard_cards: int = 0,
                 neighbour_wish: str = None, meat: int = 0, vegetarian: int = 0, vegan: int = 0, 
                 allergens: str = None, place_number: int = None, money: float = 0, payed: int = 0):
    result = database_helper.insert_student(firstname, lastname, email, number_of_tickets, number_of_hard_cards,
                                            neighbour_wish, meat, vegetarian, vegan, allergens, place_number, money, payed)
    await manager.broadcast(json.dumps(result))
    return result

@app.post("/update/")
async def update(update_data: str, condition: str):
    result = database_helper.update_student(json.loads(update_data), json.loads(condition))
    await manager.broadcast(json.dumps(result))
    return result

@app.post("/delete/")
async def delete(condition: str):
    result = database_helper.delete_student(json.loads(condition))
    await manager.broadcast(json.dumps(result))
    return result

method_map = {
    "getStudents": lambda args: database_helper.students(),
    "getSingleStudent": lambda args: database_helper.single_student(args),
    "addStudent": lambda args: database_helper.insert_student(
        args.get("firstname"), args.get("lastname"), args.get("email"), args.get("number_of_tickets"),
        args.get("number_of_hard_cards", 0), args.get("neighbour_wish"), args.get("meat", 0),
        args.get("vegetarian", 0), args.get("vegan", 0), args.get("allergens"), args.get("place_number"),
        args.get("money", 0), args.get("payed", 0)
    ),
    "updateStudent": lambda args: database_helper.update_student(args.get("update_data"), args.get("condition")),
    "deleteStudent": lambda args: database_helper.delete_student(args)
}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = websocket

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            try:
                await connection.send_text(message)
            except RuntimeError as e:
                print(f"Failed to send message: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            method_name = message.get("method")
            if method_name in method_map:
                result = method_map[method_name](message.get('args', {}))
                if result.get('type') != 'error':
                    await manager.broadcast(json.dumps(result))
                else:
                    await manager.send_personal_message(json.dumps(result), websocket)
            else:
                await manager.send_personal_message(f"Method '{method_name}' not found", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)