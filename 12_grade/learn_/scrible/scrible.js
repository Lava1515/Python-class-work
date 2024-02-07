const canvas1 = document.getElementById('drawingCanvas');
const context = canvas1.getContext('2d');
const canvas2 = document.getElementById('second_canvas');
const context2 = canvas2.getContext('2d');

// Flag to indicate whether the user is currently drawing
let isDrawing = false;

// Event listeners for mouse interactions
canvas1.addEventListener('mousedown', startDrawing);
canvas1.addEventListener('mouseup', stopDrawing);
canvas1.addEventListener('mousemove', draw);

// Function to handle the start of drawing
function startDrawing(e) {
  isDrawing = true;
  draw(e);
}

// Function to handle the end of drawing
function stopDrawing() {
  isDrawing = false;
  // Reset the drawing path
  context.beginPath();
  context2.beginPath(); // Update path on canvas2 as well
}

// Function to handle drawing based on mouse movement
function draw(e) {
  if (!isDrawing) return;

  const rect = canvas1.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const drawingData = { x, y };

  // Send drawingData to the server using fetch
  fetch('/scrible', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "drawingData": drawingData })
  });

  drawOnCanvas(context, drawingData);
}

// Function to draw on the canvas
function drawOnCanvas(_context, data) {
  // Set drawing attributes
  _context.lineWidth = 2;
  _context.lineCap = 'round';
  _context.strokeStyle = 'black';
  // Draw a line on the first canvas
  _context.lineTo(data.x, data.y);
  _context.stroke();

  // Start a new path for the next drawing segment
  _context.beginPath();
  _context.moveTo(data.x, data.y);
}

// Function to fetch data and draw on the second canvas
async function fetch_bord() {
  let data = await fetch(`/get_data`, {
    method: 'GET',
  });
  data = await data.json();
  drawOnCanvas(context2, data["drawingData"]);
}

// Fetch data and draw on the second canvas periodically
setInterval(fetch_bord, 1000);
