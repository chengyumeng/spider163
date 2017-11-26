$(function () {
    this.createDom = function () {
        this.spiderPlaylistObj = $("#spiderPlaylist");
    }
    this.documentEvent = function () {
		var self = this;
		$("#gd").click(function(){
		    $(".gdspider").css("visibility","visible");
		});
		this.spiderPlaylistObj.click(function() {
		    var gdType  = $("#gdType").val();
		    var gdPage = $("#gdPage").val();
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
	};
	this.init = function() {
	    this.createDom();
	    this.documentEvent();
	}
	this.init()

});


