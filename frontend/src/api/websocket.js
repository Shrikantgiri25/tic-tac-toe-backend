import { toast } from "react-toastify";

class GameWebSocket {
  constructor(gameId, onMessage) {
    const WS_URL = import.meta.env.VITE_API_WS_URL || 'ws://localhost:8000';
    const token = localStorage.getItem('access_token');
    const url = token ? `${WS_URL}/ws/game/${gameId}/?token=${token}` : `${WS_URL}/ws/game/${gameId}/`;
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      toast.success('Connected to game');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    this.socket.onerror = () => {
      toast.error('Connection error occurred');
    };

    this.socket.onclose = () => {
      toast.info('Disconnected from game');
    };
  }

  makeMove(position) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        action: 'make_move',
        position: position
      }));
    } else {
      toast.error('Not connected to game');
    }
  }
  
  close() {
    this.socket.close();
  }
}

export default GameWebSocket;