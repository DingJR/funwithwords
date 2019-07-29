function GoPage(pno){
        var trEle = document.getElementById("PageBreak");
        var num = trEle.getElementsByTagName('tr').length
	if(num<pageSize)return ;
        var pageSize = 15;
        var currentPage = pno;
        var totalPage = parseInt(((num-1)/pageSize) + 1)
        var startRow = (currentPage - 1) * pageSize+1;
        var endRow = (currentPage * pageSize) < num? currentPage * pageSize:num;
        for(var i=1;i<(num+1);i++){
                irow = trEle.getElementsByTagName('tr')[i-1];
                if(i>=startRow && i<=endRow){
                        irow.style.display = "table-row";
                }else{
                        irow.style.display = "none";
                }
        }
	tempStr = '<center><ul class="pagination pagination-lg">';
	if(currentPage>1){
        	tempStr += "<li><span class='btn' onClick=\"GoPage("+(1)+")\">首页</span></li>";
		tempStr += "<li><span class='btn' onClick=\"GoPage("+(currentPage - 1)+")\">&larr; 上一页</span></li>";

    	}else{
        	tempStr += "<li><span class='btn' onClick=\"GoPage("+(1)+")\">首页</span></li>";
        	tempStr += "<li class='previous disabled'><a href='javascript:void(0)'" + ">&larr; 上一页</a></li>";
    	}
	if(totalPage<=5)
    		for(var pageIndex= 1;pageIndex<totalPage+1;pageIndex++){
        		tempStr += "<li><span class='btn' onclick=\"GoPage("+(pageIndex)+")\">"+ pageIndex +"</span></li>";
    	}
	else if(currentPage+1 >= totalPage){
        	tempStr += "<li><span class='btn' onclick=\"GoPage("+ (currentPage - 2) +")\">"+ "..." +"</span></li>";
    		for(var pageIndex = totalPage-2; pageIndex <= totalPage; pageIndex++){
        		tempStr += "<li><span class='btn'  onclick=\"GoPage("+(pageIndex)+")\">"+ pageIndex +"</span></li>";
    		}
	}
	else if(currentPage <= 2){
    		for(var pageIndex = 1; pageIndex <= 4; pageIndex++){
        		tempStr += "<li><span class='btn' onclick=\"GoPage("+(pageIndex)+")\">"+ pageIndex +"</span></li>";
    		}
        	tempStr += "<li><span class='btn' onclick=\"GoPage("+ (currentPage + 2)+")\">"+ "..." +"</span></li>";
	}
	else{
        	tempStr += "<li><span class='btn' onclick=\"GoPage("+ (currentPage - 2) +")\">"+ "..." +"</span></li>";
    		for(var pageIndex = currentPage - 1; pageIndex <= currentPage + 1; pageIndex++){
        		tempStr += "<li><span class='btn' onclick=\"GoPage("+(pageIndex)+")\">"+ pageIndex +"</span></li>";
    		}
        	tempStr += "<li><span class='btn' onclick=\"GoPage("+ (currentPage + 2)+")\">"+ "..." +"</span></li>";
	}
 
    	if(currentPage<totalPage){
        	tempStr += "<li><span class='btn' onClick=\"GoPage("+(currentPage+1)+")\">下一页&rarr; </span></li>";
        	tempStr += "<li><span class='btn' onClick=\"GoPage("+(totalPage)+")\">尾页</span></li>";
    	}else{
        	tempStr += "<li class='previous disabled'><a href='javascript:void(0)'" + ">&rarr;下一页 </a></li>";
        	tempStr += "<li><span class='btn' onClick=\"GoPage("+(1)+")\">尾页</span></li>";
    	}
	tempStr += '</ul></center>';
    	document.getElementById("PageBreaker").innerHTML = tempStr;
}
