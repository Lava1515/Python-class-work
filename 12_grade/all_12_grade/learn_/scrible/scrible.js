// Get the canvas and its 2D rendering context
const canvas1 = document.getElementById('drawingCanvas');
const context = canvas1.getContext('2d');
const canvas2 = document.getElementById('second_canvas');
const context2 = canvas2.getContext('2d');
const button_f = document.getElementById('fetch_data');

button_f.onclick = fetch_bord;

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
    body: JSON.stringify(drawingData) // Wrap drawingData in an object before stringifying
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
  let data_ = await fetch(`get_data`, {
    method: 'GET',
  });
  data_ = await data_.json();
  console.log(data_);

// Loop through each point in the list and draw a circle at the coordinates
// data_.forEach(point => {
//   context2.beginPath();
//   context2.arc(point.x, point.y, 3, 0, 2);
//   context2.lineTo(point.x, point.y);
//   context2.fillStyle = 'black'; // Circle color
//   context2.fill();
//   context2.closePath();
// });
for (let i = 0; i < data_.length - 1; i++) {
  const startPoint = data_[i];
  const endPoint = data_[i + 1];
  
  context2.beginPath();
  context2.moveTo(startPoint.x, startPoint.y);
  context2.lineTo(endPoint.x, endPoint.y);
  context2.stroke();
}
}

// Fetch data and draw on the second canvas when the button is clicked
// button_f.onclick = fetch_bord; // Already assigned this in the beginning
