document.getElementById('csvFileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    console.log(file);
    const reader = new FileReader();

    reader.onload = function(event) {
        const text = event.target.result;
        const data = parseCSV(text);
        drawChart(data);
    };

    reader.readAsText(file);
});

function parseCSV(text) {
    const rows = text.split('\n').slice(1); // Skip the header row
    const dates = [];
    const closePrices = [];
    const rsiValues = [];
    const rsiMinValues = [];
    const rsiMaxValues = [];

    rows.forEach(row => {
        const cols = row.split(',');
        const date = cols[0].trim();

        if(cols[1] !== undefined && cols[7] !== undefined) {

            const closePrice = parseFloat(cols[1].trim());
            const rsi = parseFloat(cols[7].trim());

            if (!isNaN(closePrice) && !isNaN(rsi)) {
                dates.push(date);
                closePrices.push(closePrice);
                rsiValues.push(rsi);
                rsiMinValues.push(30);
                rsiMaxValues.push(70);
            }
        }
    });

    return { dates, closePrices, rsiValues, rsiMinValues, rsiMaxValues };
}

function drawChart(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Close Price',
                    data: data.closePrices,
                    borderColor: 'blue',
                    fill: false,
                    yAxisID: 'y',
                },
                {
                    label: 'RSI',
                    data: data.rsiValues,
                    borderColor: 'rgba(255, 99, 132, 0.5)',
                    fill: false,
                    yAxisID: 'y1',
                },
                {
                    label: 'RSI MIN',
                    data: data.rsiMinValues,
                    borderColor: 'green',
                    fill: true,
                    yAxisID: 'y3',
                },
                {
                    label: 'RSI MAX',
                    data: data.rsiMaxValues,
                    borderColor: 'red',
                    fill: true,
                    yAxisID: 'y4',
                }
            ],
        },
        options: {
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Close Price',
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'RSI',
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    min: 0,
                    max: 100
                },
                y3: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'RSI MIN',
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    display: false,
                    min: 0,
                    max: 100
                },
                y4: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'RSI MAX',
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    display: false,
                    min: 0,
                    max: 100
                }
            }
        }
    });
}
