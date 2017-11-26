$(function () {
    this.createDom = function () {
        this.spiderPlaylistObj = $("#spiderPlaylist");
    }
    this.documentEvent = function () {
		var self = this;
		this.spiderPlaylistObj.click(function() {
		    var gdType  = $("#gdType").val();
		    var gdCount = $("#gdCount").val();
		    $('#gdModal').modal('hide')
		    $.ajax({
                url : "/spider/getPlaylist",
                data:"gdType="+gdType+"&gdCount="+gdCount,
                type:"post",
                dataType : "json",
                success : function (data) {
                    alert(data["test"]);
                },
            });
		});
	};

	this.createCharts = function() {
	      dataCount()
	      playlist()
	      music()
          setInterval(dataCount,10000);
          setInterval(playlist,1000000);
          setInterval(music,1000000);
	}
	this.init = function() {
	    this.createDom();
	    this.documentEvent();
	    this.createCharts();
	}
	this.init()

});

function dataCount() {
    $.ajax({
                url : "/stat/dataCount",
                type:"get",
                dataType : "json",
                success : function (data) {
                    var name = {"countPlaylist":"歌单抓取","countLyric":"歌词抓取","countComment":"评论抓取"};
                    for (k in data){
                        var chart = echarts.init(document.getElementById(k), 'macarons');
                            var  option = {
                                tooltip : {formatter: "{a} <br/>{b} : {c}%"},
//                                toolbox: {feature: {restore: {},saveAsImage: {}}},
                                series: [
                                {
                                    name: k,
                                    type: 'gauge',
                                    detail: {formatter:'{value}%'},
                                    data: [{value: data[k], name: name[k]}]
                                }
                             ]};
                        chart.setOption(option);
                    }
                },
         });
}

function playlist() {
    $.ajax({
                url : "/stat/playlist",
                type:"get",
                dataType : "json",
                success : function (data) {
                    for (k in data){
                        var chart = echarts.init(document.getElementById(k), 'macarons');
                        var t = [];
                        var v = [];
                        for (d in data[k]) {
                            t.push(data[k][d][0]);
                            v.push(data[k][d][1]);
                        }
                        var option = {
                            title: {text: k},
                            tooltip: {},
                            legend: {data:['数量']},
                            xAxis: {data: t},
                            yAxis: {},
                            series: [{name: '数量',type: 'bar',data: v }]
                            };
                        chart.setOption(option);
                    }
                },
         });



}

function music() {
    $.ajax({
                url : "/stat/music",
                type:"get",
                dataType : "json",
                success : function (data) {
                    for (k in data){
                        var chart = echarts.init(document.getElementById(k), 'macarons');
                        var t = [];
                        var v = [];
                        for (d in data[k]) {
                            t.push(data[k][d][0]);
                            v.push(data[k][d][1]);
                        }
                        var option = {
                            title: {text: k},
                            tooltip: {},
                            legend: {data:['评论数量']},
                            xAxis: {data: t,
                                axisLabel:{
                                    interval:0,
                                    rotate:45,//倾斜度 -90 至 90 默认为0
                                    margin:4,
                                },
                            },
                            yAxis: {},
                            series: [{name: '评论数量',type: 'bar',data: v }]
                            };
                        chart.setOption(option);
                    }
                },
         });
}