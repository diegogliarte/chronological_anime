var data = null

google.charts.load("current", {packages: ["timeline"]});
google.charts.setOnLoadCallback(function() {drawChart(data)});

function setData(data_) {
    data = data_
}

function drawChart(data) {
      data = JSON.parse(data)
      var container = document.getElementById('event-timeline');
      var chart = new google.visualization.Timeline(container);
      var dataTable = new google.visualization.DataTable();
      dataTable.addColumn({type: 'string', id: 'Type'});
      dataTable.addColumn({type: 'string', id: 'Name'});
      dataTable.addColumn({type: 'date', id: 'Start'});
      dataTable.addColumn({type: 'date', id: 'End'});
      data.forEach(anime => {
          var type = anime.type
          var name = anime.name
          var date_start = new Date(anime.date_start.split(" "))
          var date_end = new Date(anime.date_end.split(" "))
          if (date_start.getTime() != date_end.getTime()) {
              dataTable.addRow([type, name, date_start, date_end])
          }
      })

      data.forEach(anime => {
          var type = anime.type
          var name = anime.name
          var date_start = new Date(anime.date_start.split(" "))
          var date_end = new Date(anime.date_end.split(" "))
          if (date_start.getTime() === date_end.getTime()) {
              dataTable.addRow([type, name, date_start, date_end])
          }
      })


      var options = {
          hAxis: {
              maxValue: new window.Date()
          },
          timeline: {singleColor: '#1f1f1f'},
          backgroundColor: '#efefef',
          avoidOverlappingGridLines: false,
          height: 512,
      };

      var observer = new MutationObserver(setBorderRadius);
      google.visualization.events.addListener(chart, 'ready', function () {
          var labels = container.getElementsByTagName('text');
          setLabelColor(labels);
          setBorderRadius();
          observer.observe(container, {
              childList: true,
              subtree: true
          });
      });

      function setLabelColor(labels) {
          Array.prototype.forEach.call(labels, function (label) {
              if (label.getAttribute('text-anchor') === 'middle') {
                  label.setAttribute('fill', '#efefef');
              }
          });
      }

      function setBorderRadius() {
          let i = 0
          Array.prototype.forEach.call(container.getElementsByTagName('rect'), function (rect) {
              if (parseFloat(rect.getAttribute('x')) > 0) {
                  if (dataTable.getValue(i, 2).getTime() === dataTable.getValue(i, 3).getTime()) {
                      rect.classList.add("dot")
                  }
                  i++
              }

          });
      }

      chart.draw(dataTable, options);
  }