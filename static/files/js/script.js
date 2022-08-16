var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
  if(!sidebarOpen) {
    sidebar.classList.add("sidebar-responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if(sidebarOpen) {
    sidebar.classList.remove("sidebar-responsive");
    sidebarOpen = false;
  }
}

const xhttp = new XMLHttpRequest();

// Define a callback function
xhttp.onload = function() {
  var a = JSON.parse(xhttp.response)
  fgraph = a.first
 
  var barChartOptions = {
    series: [{
      data: Object.values(a.first)
    }],
    chart: {
      type: 'bar',
      height: 350,
      toolbar: {
        show: false
      },
    },
    colors: [
      "#21232d",
      "#21232d",
      "#21232d"
      
    ],
    plotOptions: {
      bar: {
        distributed: true,
        borderRadius: 4,
        horizontal: false,
        columnWidth: '40%',
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: {
      show: false
    },
    xaxis: {
      categories: ["Furniture", "Office Supplies", "Technology"],
    },
    yaxis: {
      title: {
        text: "Profit"
      }
    }
  };
  
  var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
  barChart.render();


  //Area Chart
  var areaChartOptions = {
    series: [{
      name: 'Profit',
      data: Object.values(a.first)
    }, {
      name: 'Sales',
      data: Object.values(a.second)
    }],
    chart: {
      height: 350,
      type: 'area',
      toolbar: {
        show: false,
      },
    },
    colors: ["#21232d", "#818589"],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth'
    },
    labels: ["Furniture", "Office Supplies", "Technology"],
    markers: {
      size: 0
    },
    yaxis: [
      {
        title: {
          text: 'Profit across categories',
        },
      },
      {
        opposite: true,
        title: {
          text: 'Sales across categories',
        },
      },
    ],
    tooltip: {
      shared: true,
      intersect: false,
    }
  };
  
  var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
  areaChart.render();

  var barChartOptions = {
    series: [{
      data: Object.values(a.third)
    }],
    chart: {
      type: 'bar',
      height: 350,
      toolbar: {
        show: false
      },
    },
    colors: [
      "#21232d",
      "#21232d",
      "#21232d"
      
    ],
    plotOptions: {
      bar: {
        distributed: true,
        borderRadius: 4,
        horizontal: true,
        columnWidth: '40%',
      }
    },
    dataLabels: {
      enabled: false
    },
    legend: {
      show: false
    },
    xaxis: {
      categories: ["First class", "Same Day", "Second class", "Standard Class"],
    },
    yaxis: {
      title: {
        text: "Profit distribution over ship mode"
      }
    }
  };
  
  var barChart = new ApexCharts(document.querySelector("#pie-chart"), barChartOptions);
  barChart.render();

  var areaChartOptions = {
    series: [{
      name: 'Profit',
      data: [484247.4981000009, 470532.50899999985, 609205.5980000008, 733215.2551999999]
    }],
    chart: {
      height: 350,
      type: 'area',
      toolbar: {
        show: false,
      },
    },
    colors: ["#21232d"],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: 'smooth'
    },
    labels: ["2014", '2015', '2016', '2017'],
    markers: {
      size: 0
    },
    yaxis: [
      {
        title: {
          text: 'Profit across years',
        },
      },
      
    ],
    tooltip: {
      shared: true,
      intersect: false,
    }
  };
  
  var areaChart = new ApexCharts(document.querySelector("#bar-chart2"), areaChartOptions);
  areaChart.render();


  
}

// Send a request
xhttp.open("GET", "/getdata");
xhttp.send();

const xhttp1 = new XMLHttpRequest();

// Define a callback function
xhttp1.onload = function() {
  console.log(xhttp1.response)
}

// Send a request
xhttp1.open("GET", "/getyeardata");
xhttp1.send();


// ---------- CHARTS ----------

// BAR CHART



// AREA CHART


