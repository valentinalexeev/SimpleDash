var charts = [];

function chartInit(config) {
    $.ajax({
        url: config.datasource + "/config",
        dataType: "text json",
        contentType: "application/json; charset=utf-8",
        context: config
    }).done(function(data) { chartConfigLoaded($(this)[0], data);})
    .error(function (jqXHR, textStatus, errorThrown) {
        alert (textStatus);
        alert (errorThrown);
    });
    
    charts.push(config);
}

function chartConfigLoaded(config, data) {
    data.config.chart = {
        type: config.type,
        renderTo: config.renderTo
    };
    data.config.credits = {"enabled": false };

    config.chart = new Highcharts.Chart(data.config);
    $.ajax({
        url: config.datasource + "/data",
        dataType: "text json",
        contentType: "application/json; charset=utf-8",
        context: config
    }).done(function(data){chartDataLoaded($(this)[0], data)})
    .error(function (jqXHR, textStatus, errorThrown) {
        alert (textStatus);
        alert (errorThrown);
    });

}

function chartDataLoaded(config, data) {
    for (var i = 0; i < data.data.length; i++) {
        config.chart.addSeries(data.data[i]);
    }
}