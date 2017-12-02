$(function () {
    this.createDom = function(){
    }
    this.documentEvent = function(){

    }
    this.init = function() {
        commentlist()
    }
    this.init()
});
function commentlist() {
    $.ajax({
                url : "/scan/data",
                type:"get",
                dataType : "json",
                success : function (data) {
                    code = "";
                    for ( i in data['comment']) {
                        c = data['comment'][i];
                        code = code + "<div class=\"col-md-5 col-sm-4 col-xs-6 i-c-item\">"
                        + "<a title=\""+ c["song"]["name"]+"\" target=\"_blank\" href=\"http://music.163.com/#/song?id=" + c["song"]["id"]+ "\"><div class=\"i-c-p i-c-p3\"><h2 class=\"i-c-ph\">"
                        + c["song"]["name"] + " - " + c["song"]["author"] + "</h2></div></a>"
                        + "<p class=\"navbar-text\">" + c["txt"] + "</p>"
                        + "<div style=\"position: absolute\"><small><span class=\"glyphicon glyphicon-user\" aria-hidden=\"true\">  " + c["author"] + "</span>  <span class=\"glyphicon glyphicon-heart\" aria-hidden=\"true\"> " + c["like"] + "</span>"  + "</small></div></div>"
                    }
                    $("#index-group").html(code);

                }
         });
}
