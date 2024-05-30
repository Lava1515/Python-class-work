document.addEventListener('DOMContentLoaded', (event) => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const numColumns = 100;
    const initialData = Array(numColumns).fill(0);

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({ length: numColumns }, (_, i) => i + 1),
            datasets: [{
                label: 'Histogram Data',
                data: initialData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateHistogram(newValue) {
        // Shift data to the left and add new value at the end
        chart.data.datasets[0].data.shift();
        chart.data.datasets[0].data.push(newValue);

        // Update the chart
        chart.update();
    }

    // Example of adding new data every second
    setInterval(() => {
        const newValue = Math.floor(Math.random() * 1000);  // Replace with your data source
        updateHistogram(newValue);
    }, 1000);
});
