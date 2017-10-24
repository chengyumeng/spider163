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
	this.init = function() {
	    this.createDom();
	    this.documentEvent();
	}
	this.init()

});


