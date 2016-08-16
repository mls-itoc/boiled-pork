// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or any plugin's vendor/assets/javascripts directory can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// compiled file. JavaScript code in this file should be added after the last require_* statement.
//
// Read Sprockets README (https://github.com/rails/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require jquery
//= require jquery_ujs

//= require_tree .
$(function() {
  $("#current-date").val(get_today())
  var width = 300,
    height = 370;

  var svg = d3.select("#main").append("svg")
    .attr("width", width)
    .attr("height", height);

  var projection = d3.geo.mercator()
    .center([136, 35.5])
    .scale(750)
    .translate([width / 2, height / 2]);

  var path = d3.geo.path()
    .projection(projection);


  var pref_deffered = get_json("/prefs")

  pref_deffered.done(function(res) {
    var pref = res;
    var predict_deffered = get_json("/prediction/fetch_prediction", { date: get_today() })

    predict_deffered.done(function(res) {
      var predict = res; //mock();

      d3.json("/japan.json", function(error, japan) {
        var topo = topojson.feature(japan, japan.objects.pref).features;
        svg.selectAll(".pref")
          .data(topo)
          .enter()
          .append("path")
          .attr("class", function(d) {
            return "pref pref" + pref[d.properties.name_local];
          })
          .attr("d", path);

        for (var key in predict) {
          var color = predict[key];
          var color1 = 255;
          var color2 = 255
          if (color == 1) {
            color1 = 235;
            color2 = 76
          }
          d3.select(".pref" + key)
            .transition()
            .style("fill", "rgb(255, " + color1 + ", " + color2 + ")");
        } // 255 235 76

      });
    });
  });

  pref_deffered.fail(function() {
    alert("都道府県情報の取得に失敗しました。")
  });

  pref_deffered.always(function() {
    console.log("Done: Get Pref")
  });

  $("#current-date").on("change", function(e) {
    var date = e.target.value
    var predict_deffered = get_json("/prediction/fetch_prediction", { date: date });
    predict_deffered.done(function(res) {
      var predict = res; //mock2();
      for (var key in predict) {
        var color = predict[key];
        var color1 = 255;
        var color2 = 255
        if (color == 1) {
          color1 = 235;
          color2 = 76
        }
        d3.select(".pref" + key)
          .transition()
          .style("fill", "rgb(255, " + color1 + ", " + color2 + ")");
      } // 255 235 76
    });

    predict_deffered.fail(function(res){
      alert("予測データの取得に失敗しました。")
    });

    predict_deffered.always(function() {
      console.log("Done: Get Prediction")
    });
  });

});

function get_today() {
  var today = new Date();
  var year = today.getFullYear();
  var month = (today.getMonth() + 1);
  month = ('0' + month).slice(-2);
  var date = today.getDate();
  date  = ('0' + date).slice(-2);
  return year + "-" + month + "-" + date
}

function get_json(url, params) {
  var xhr = $.ajax({
    type: "GET",
    url: url,
    dataType: "json",
    data: params
  });
  return xhr
}

function mock() {
  return {
      "1": 0,
      "2": 1,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 1,
      "8": 1,
      "9": 1,
      "10": 0,
      "11": 0,
      "12": 0,
      "13": 0,
      "14": 0,
      "15": 1,
      "16": 1,
      "17": 0,
      "18": 0,
      "19": 0,
      "20": 1,
      "21": 1,
      "22": 0,
      "23": 1,
      "24": 1,
      "25": 1,
      "26": 1,
      "27": 0,
      "28": 0,
      "29": 0,
      "30": 1,
      "31": 0,
      "32": 0,
      "33": 0,
      "34": 1,
      "35": 0,
      "36": 1,
      "37": 1,
      "38": 1,
      "39": 0,
      "40": 0,
      "41": 0,
      "42": 1,
      "43": 0,
      "44": 1,
      "45": 1,
      "46": 1,
      "47": 0
    }
}


function mock2() {
  return {
      "1": 1,
      "2": 0,
      "3": 1,
      "4": 1,
      "5": 1,
      "6": 1,
      "7": 0,
      "8": 0,
      "9": 0,
      "10": 1,
      "11": 1,
      "12": 1,
      "13": 1,
      "14": 1,
      "15": 0,
      "16": 0,
      "17": 1,
      "18": 1,
      "19": 1,
      "20": 0,
      "21": 0,
      "22": 1,
      "23": 0,
      "24": 0,
      "25": 0,
      "26": 0,
      "27": 1,
      "28": 1,
      "29": 1,
      "30": 0,
      "31": 1,
      "32": 1,
      "33": 1,
      "34": 0,
      "35": 1,
      "36": 0,
      "37": 0,
      "38": 0,
      "39": 1,
      "40": 1,
      "41": 1,
      "42": 0,
      "43": 1,
      "44": 0,
      "45": 0,
      "46": 0,
      "47": 1
    }
}
