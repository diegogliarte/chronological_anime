google.charts.load("current", {packages:["timeline"]});

function drawChart(data) {
    data_new = JSON.parse(data)
    data_new.forEach(obj => {
        console.log(obj)
    })
    var container = document.getElementById('event-timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'Type' });
    dataTable.addColumn({ type: 'string', id: 'Name' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      [ 'TV', 'Dragon Ball', new Date(1986, 2, 26), new Date(1989, 4, 12), ],
      [ 'TV', 'Dragon Ball Z', new Date(1989, 4, 26), new Date(1996, 1, 31) ],
      [ 'TV', 'Dragon Ball Super', new Date(2015, 7, 5), new Date(2018, 3, 25) ],
            [ 'Movie', 'Dragon Ball Movie 1: Shen Long no Densetsu', new Date(1986, 12, 20), new Date(1986, 12, 20) ],
      [ 'Movie', 'Dragon Ball Movie 2: Majinjou no Nemurihime', new Date(1987, 7, 18), new Date(1987, 7, 18) ],
    ]);



    var options = {
        timeline: { singleColor: '#1f1f1f' },
        backgroundColor: '#efefef',
        avoidOverlappingGridLines: false
      };

    var observer = new MutationObserver(setBorderRadius);
    google.visualization.events.addListener(chart, 'ready', function () {
    setBorderRadius();
    observer.observe(container, {
      childList: true,
      subtree: true
    });
    });

    function setBorderRadius() {
    let i = 0
    Array.prototype.forEach.call(container.getElementsByTagName('rect'), function (rect) {
      if (parseFloat(rect.getAttribute('x')) > 0) {
        if (dataTable.getValue(i, 2).getTime() == dataTable.getValue(i, 3).getTime()) {
          rect.setAttribute('rx', 20);
          rect.setAttribute('ry', 20);
          rect.setAttribute('width', 20),
          rect.setAttribute('height', 20)
        }
        i++
      }

    });
    }

    chart.draw(dataTable, options);
}

