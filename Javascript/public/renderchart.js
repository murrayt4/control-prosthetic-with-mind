var chartData;

$(function(){
  $.ajax({

    url: '/notes',
    type: 'GET',
    success : function(data) {
      chartData = data;

      var chartProperties = {
        "caption": "Number of Blinks vs. Time",
        "xAxisName": "Time",
        "yAxisName": "Number of Blinks",
        "showValues":"0",
        "drawAnchors":"0"
      };

      var categoriesArray = [{
          "category" : data["categories"]
      }];

      var lineChart = new FusionCharts({
        type: 'line',
        renderAt: 'chart-location',
        width: '1000',
        height: '600',
        dataFormat: 'json',
        dataSource: {
          chart: chartProperties,
          categories : categoriesArray,
          dataset : data["dataset"]
         /* data: [
        {
        "label" : "Mon",
        "value" : "1234"
        },
        {
        "label" : "Tue",
        "value" : "23532"
        }
        ],*/
        }
      });
            lineChart.render();
    }
  });
});


