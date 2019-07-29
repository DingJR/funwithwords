function complete(formname){
        var searchform = "#" + formname.getAttribute('id')
        $.ajax({
             url : "/autoComplextion/",
             type : "post",
             data : {localName : $(searchform).val()},
             dataType : "json",
             success: function( jsonData ) {
                var data = eval(jsonData);
                var context = [];
                $.map( data, function( item ) {
                        var name = item.localName;
                        //context = context + "<p><span class='append_span' onclick=select('"+name+"')>"+name+"</span></p>";
                        context.push(name);
                });
                $(searchform).html(""); 
                $(searchform).autocomplete({
                        source: context,
			select: function( event, ui ) {
				$(searchform).val( ui.item.value.split(' ')[0]);
            			return false;
          			},
			focus:  function( event, ui ) {
				$(searchform).val( ui.item.value.split(' ')[0]);
				return false;
				}
        	});
		context = [];
            }
       });
};

