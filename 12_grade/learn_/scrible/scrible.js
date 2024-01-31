const canvas = new fabric.Canvas('canvas', { isDrawingMode: true });

const socket = new WebSocket('ws://localhost:8765');

socket.addEventListener('message', (event) => {
  // Draw received data on the canvas
  const data = JSON.parse(event.data);
  if (data.type === 'path') {
    const path = new fabric.Path(data.path, {
      stroke: data.stroke,
      strokeWidth: data.strokeWidth,
    });
    canvas.add(path);
    canvas.renderAll();
  }
});

canvas.on('path:created', (event) => {
  // Send drawing data to the server
  const path = event.path;
  const data = {
    type: 'path',
    path: path.path,
    stroke: path.stroke,
    strokeWidth: path.strokeWidth,
  };
  socket.send(JSON.stringify(data));
});
