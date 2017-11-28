$(function () {
    this.createDom = function () {
        this.spiderPlaylistObj = $("#spiderPlaylist");
        this.SpiderMusicObj    = $("#spiderMusic");
        this.SpiderLyricObj    = $("#spiderLyric");
        this.SpiderCommentObj  = $("#spiderComment");
    }
    this.documentEvent = function () {
		var self = this;
		 this.hideBox = function() {
		    $(".gdspider").css({"display":"none"});
		    $(".gqspider").css({"display":"none"});
		    $(".gcspider").css({"display":"none"});
		    $(".rpspider").css({"display":"none"});
		}
		$("#gd").click(function(){
		    self.hideBox();
		    $(".gdspider").css({"display":"block"});
		});
		$("#gq").click(function(){
		    self.hideBox();
		    $(".gqspider").css({"display":"block"});
		});
		$("#gc").click(function(){
		    self.hideBox();
		    $(".gcspider").css({"display":"block"});
		});

		$("#rp").click(function(){
		    self.hideBox();
		    $(".rpspider").css({"display":"block"});
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

		this.SpiderLyricObj.click(function() {
		    var gqCount  = $("#gqCount").val();
		    $.ajax({
                url : "/spider/getLyric",
                data:"gqCount="+gqCount,
                type:"post",
                dataType : "json",
                success : function (data) {
                var thead = " <thead><tr><th>#</th><th>歌曲名字</th><th>作者</th><th>评论数量</th></tr></thead>";
                var tbody = "";
                for (cnt in data['data']) {
                        tbody = tbody + "<tr><th scope=\"row\">" + cnt
                        + "</th>"
                        +"<td>"+ data['data'][cnt]["name"] + "</td>"
                        + "<td>"+ data['data'][cnt]["author"] + "</td>"
                        +"<td>"+ data['data'][cnt]["comment"] + "</td>"
                        +"</tr>";
                }
                $("#printTable").html(thead + "<tbody>" + tbody + "</tbody>");
                },
            });
		});

		this.SpiderCommentObj.click(function() {
		    var gqCount  = $("#gqCount-1").val();
		    $.ajax({
                url : "/spider/getComment",
                data:"gqCount="+gqCount,
                type:"post",
                dataType : "json",
                success : function (data) {
                var thead = " <thead><tr><th>#</th><th>歌曲名字</th><th>作者</th><th>ID</th></tr></thead>";
                var tbody = "";
                for (cnt in data['data']) {
                        tbody = tbody + "<tr><th scope=\"row\">" + cnt
                        + "</th>"
                        +"<td>"+ data['data'][cnt]["name"] + "</td>"
                        + "<td>"+ data['data'][cnt]["author"] + "</td>"
                        +"<td>"+ data['data'][cnt]["song_id"] + "</td>"
                        +"</tr>";
                }
                $("#printTable").html(thead + "<tbody>" + tbody + "</tbody>");
                },
            });
		});


	};
	this.init = function() {
	    this.createDom();
	    this.documentEvent();
	}
	this.init()

});


