// Servicio de comunicación bidireccional con Reflex (WebSocket)
// Permite enviar y recibir mensajes entre el frontend 3D y el backend Python

class ReflexConnection {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.onMessage = null;
    this.onOpen = null;
    this.onClose = null;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = (event) => {
      if (this.onOpen) this.onOpen(event);
    };
    this.ws.onmessage = (event) => {
      if (this.onMessage) this.onMessage(JSON.parse(event.data));
    };
    this.ws.onclose = (event) => {
      if (this.onClose) this.onClose(event);
    };
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

export default ReflexConnection; 