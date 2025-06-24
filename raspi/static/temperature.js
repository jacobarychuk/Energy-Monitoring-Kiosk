// Chart of historical temperature data
var chartTemperatureHistory = new Highcharts.stockChart({
  chart: {
    renderTo: 'chart-temperature-history',
    zooming: {
      mouseWheel: { enabled: false },
    },
  },
  time: { useUTC: false },
  title: {
    text: 'Historical Temperatures',
    style: {
      fontSize: '1.2rem',
      fontFamily: 'Verdana',
    },
  },
  legend: {
    enabled: true,
    itemStyle: {
      fontFamily: 'Verdana',
    },
  },
  navigator: { enabled: false },
  scrollbar: { enabled: false },
  rangeSelector: {
    buttons: [
      { type: 'all', text: 'All' },
      { type: 'day', count: 1, text: '1d' },
      { type: 'hour', count: 1, text: '1h' },
      { type: 'minute', count: 1, text: '1m' },
    ],
    selected: 0, // Start with "All" selected by default
    inputEnabled: true, // Allows manual date typing
    labelStyle: { fontFamily: 'Verdana' },
    inputStyle: { fontFamily: 'Verdana' },
    buttonTheme: {
      style: { fontFamily: 'Verdana' },
    },
  },
  series: [
    {
      type: "line",
      showInLegend: true,
      name: "Glycol",
      color: "#1f77b4",
      dashStyle: "Dot",
      data: []
    },
    {
      type: "line",
      showInLegend: true,
      name: "Preheat",
      color: "#ff7f0e",
      dashStyle: "Dash",
      data: []
    },
    {
      type: "line",
      showInLegend: true,
      name: "Ambient",
      color: "#2ca02c",
      dashStyle: "ShortDash",
      data: []
    },
    {
      type: "line",
      showInLegend: true,
      name: "Source",
      color: "#17becf",
      dashStyle: "DashDot",
      data: []
    },
    {
      type: "line",
      showInLegend: true,
      name: "Hot",
      color: "#d62728",
      dashStyle: "Solid",
      data: []
    },
  ],
  tooltip: {
    style: { fontFamily: 'Verdana' },
  },
  plotOptions: {
    line: {
      dataLabels: { enabled: false },
      marker: { enabled: false },
    },
  },
  xAxis: {
    title: {
      text: 'Time',
      style: { fontFamily: 'Verdana' },
    },
    type: 'datetime',
    labels: {
      style: { fontFamily: 'Verdana' },
    },
  },
  yAxis: {
    title: {
      text: 'Temperature (Celsius)',
      style: { fontFamily: 'Verdana' },
    },
    opposite: false,
    labels: {
      style: { fontFamily: 'Verdana' },
    },
  },
  credits: { enabled: false },
});

const fetchAllTemperatureData = () => {
  const now = Math.floor(Date.now() / 1000); // Unix seconds
  const start = 0;
  const end = now;

  fetch(`/temperature-range?start=${start}&end=${end}`)
    .then(response => {
      return response.json();
    })
    .then(data => {

      // Check if any of the series have data
      const hasData = data.glycol && data.glycol.length > 0;
      if (!hasData) {
        return;
      }

      chartTemperatureHistory.series[0].setData(data.glycol);
      chartTemperatureHistory.series[1].setData(data.preheat);
      chartTemperatureHistory.series[2].setData(data.ambient);
      chartTemperatureHistory.series[3].setData(data.source);
      chartTemperatureHistory.series[4].setData(data.hot);
    })
    .catch(error => {
      console.error("Error fetching historical data:", error);
    });
};

fetchAllTemperatureData();

const chartTemperatureHistoryButtons = chartTemperatureHistory.rangeSelector.buttons;
chartTemperatureHistoryButtons.forEach((button, i) => {
  button.element.addEventListener('click', () => {
    if (i === 0) { // "All" is selected
      fetchAllTemperatureData();
    }
  });
});
