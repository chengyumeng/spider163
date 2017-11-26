$(function () {
    this.createDom = function () {
        this.spiderPlaylistObj = $("#spiderPlaylist");
        this.SpiderMusicObj    = $("#spiderMusic");
    }
    this.documentEvent = function () {
		var self = this;
		$("#gd").click(function(){
		    $(".gdspider").css("visibility","visible");
		});
		$("#gq").click(function(){
		    $(".gdspider").css("visibility","hidden");
		    $(".gqspider").css("visibility","visible");
		});
		this.spiderPlaylistObj.click(function() {
		    var gdType  = $("#gdType").val();
		    var gdPage  = $("#gdPage").val();
		    $.ajax({
                url : "/spider/getPlaylist",
                data:"gdType="+gdType+"&gdPage="+gdPage,
                type:"post",
                dataType : "json",
                success : function (data) {
                var thead = " <thead><tr><th>#</th><th>歌单名字</th></tr></thead>";
                var tbody = "";
                for (t in data['title']) {
                    tbody = tbody + "<tr><th scope=\"row\">"+ t +"</th><td>"+ data['title'][t]  +"</td></tr>";
                }
                     $("#printTable").html(thead + "<tbody>" + tbody + "</tbody>");
                },
            });
		});

		this.SpiderMusicObj.click(function() {
		    var gdSource = $("#gdSource").val();
		    var gdCount  = $("#gdCount").val();
		    for (i=0;i< gdCount; i++ ){
		        $.ajax({
                url : "/spider/getMusic",
                data:"gdSource="+gdSource,
                type:"post",
                dataType : "json",
                success : function (data) {
                var thead = " <thead><tr><th>#</th><th>歌单名字</th><th>歌曲名字</th><th>作者</th></tr></thead>";
                var tbody = "";
                for (playlist in data['data']) {
                    for ( m in data['data'][playlist]) {
                        tbody = tbody + "<tr><th scope=\"row\">"
                        + "</th><td>"+ playlist  +"</td>"
                        +"<td>"+ data['data'][playlist][m]["name"] + "</td>"
                        + "<td>"+ data['data'][playlist][m]["author"] + "</td>"
                        +"</tr>";
                    }
                }
                if((data['data'][playlist]).length > 0) {
                    $("#printTable").html(thead + "<tbody>" + tbody + "</tbody>");
                }
                },
            });
		    }
		});


	};
	this.init = function() {
	    this.createDom();
	    this.documentEvent();
	}
	this.init()

});


