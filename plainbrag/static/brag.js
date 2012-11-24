
YUI().use("datatable-base", "json-parse", "io-base", function(Y) {
    var jsonString = Y.one('#prodjson')._node.value;
    var jsondata;
    try {
        jsondata = Y.JSON.parse(jsonString);
    }
    catch (e) {
	alert("Invalid product data");
    }

    var getLink = function (o) {
        var title  = o.record.getValue("publish_title");
	if (title === "--"){
	    return title;
	}
	var link = '<span class=\"publish-button\"><input value=\"publish\" type=\"submit\" onClick=\'publishIt('+title+')\'/> </span>';

	return link;
    };

    var datacount = jsondata.__count__;
    if(datacount < 1){
       jsondata =[{ date: "--", price: "--", publish_title: "--", title : "--"}];
    }

    var cols = [{key:"title",label:"Title"},{key:"price",label:"Price"},
    {key:"date",label:"Date"},{key:"publish",label:"Publish",formatter:getLink}],
    data = jsondata,
    dt = new Y.DataTable.Base({
	    columnset: cols,
	    recordset: data,
	    summary: "Products list"
	}).render("#recent-buys");


    var addRowBtn = Y.one("#addprod");
    addRowBtn.on('click', function(e) {
	    //before calling addItem, make HTTP POST, and update
	    //prodjson div with the new json
	    sendData();
	    //addItem();
	    });

    var addItem = function() {
	var o = {}, 
	title = Y.one('#title'),
        link = Y.one('#link'),
	price = Y.one('#price');
	image_link = Y.one("#image_link");
	day = Y.one("#date_day");
	month = Y.one("#date_month");
	year = Y.one("#date_year");
		     
        title.set("value", "");
	link.set("value", "");
	price.set("value", "");
	image_link.set("value", "");
	day.set("value", "");
	month.set("value", "");
	year.set("value", "");
	//instead of this, update data with new prodjson string
	//instead of push
       	//data.push(o);
	var jsonString = Y.one('#prodjson')._node.value;
	var jsondata;
	try {
	    jsondata = Y.JSON.parse(jsonString);
	    //alert ("json string = "+jsonString);
	}
	catch (e) {
	    //alert("Invalid product data");
	}
	data=jsondata;
       	dt.set('recordset', data).render();
       	dt.render();
    };

    var sendData = function() {
 
	var div = Y.one('#prodjson');
	var user_id = Y.one("#user_id")._node.value;
	var csrf = Y.one("#csrf")._node.value;
	var title = Y.one("#title")._node.value;
	var link = Y.one("#link")._node.value;
	var image_link = Y.one("#image_link")._node.value;
	var price = Y.one("#price")._node.value;
	var day = Y.one("#date_day")._node.value;
	var month = Y.one("#date_month")._node.value;
	var year = Y.one("#date_year")._node.value;
	var dataString = 'user_id='+ user_id +'&csrf='+csrf+'&title='+title+'&link='; 
	dataString += '&link='+link+'&image_link='+image_link+'&price='+price; 
	dataString += '&date_year='+year+'&date_month='+month+'&date_day='+day
 
	var handleSuccess = function(ioId, o){
	    Y.log(arguments);
	    Y.log("The success handler was called.  Id: " + ioId + ".", "info", "example");
 
	    if(o.responseText !== undefined){
		//alert("Success : "+o.responseText);
		div.set("innerHTML", o.responseText);
		addItem();
	    }
	}
 
	var handleFailure = function(ioId, o){
	    Y.log("The failure handler was called.  Id: " + ioId + ".", "info", "example");
	    if(o.responseText !== undefined){
		//var jsObj = JSON.parse(o.responseText);
		alert("Failed : ");
	    }
	}
 
	Y.on('io:success', handleSuccess);
	Y.on('io:failure', handleFailure);
 
	var cfg = {
	    method: "POST",
	    data: dataString
	};
 
	var sUrl = "/addproduct/";
 
	function makeRequest(){
	    //alert('clicked : '+cfg.data);
	    var request = Y.io(sUrl, cfg);
	    Y.log("Initiating request; Id: " + request.id + ".", "info", "example");
	}

	//alert('clicked : '+cfg.data);
	var request = Y.io(sUrl, cfg);
	Y.log("Initiating request; Id: " + request.id + ".", "info", "example");
 
	//Y.on("click", makeRequest, "#acompile");
 
	Y.log("As you interact with this example, relevant steps in the process will be logged here.", "info", "example");
    }
});


/*
YUI().use("datasource-get", "datasource-jsonschema", "datatable-base", "datatable-datasource", function (Y) {

var url = "/",
    query = "getproducts/750960780?a=b",
    dataSource,
    table;

dataSource = new Y.DataSource.Get({ source: url });

dataSource.plug(Y.Plugin.DataSourceJSONSchema, {
	schema: {
	    resultListLocator: "query.results.Result",
		resultFields: [
		      "title",
		       "date",
		       "price"
		       ]
		}
    });

dataSource.sendRequest({
    callback: {
	success: function(e) {
	    Y.log('logging now : ');
	    Y.log(e);
	}
    }
});

table = new Y.DataTable.Base({
	columnset: [
		    "Date",
		    "Price",
		    "Title",
		    ],
	summary: "My Products",
	caption: "Products I bought"
    });

table.plug(Y.Plugin.DataTableDataSource, { datasource: dataSource });

table.render("#recent-buys1");

table.datasource.load({ request: query });
});
*/




YUI({ filter: 'raw' }).use("yui", "tabview", function(Y) {
    var tabview = new Y.TabView({srcNode:'#buys'});
    tabview.render();
});

YUI({filter:'raw'}).use('autocomplete', 'autocomplete-filters', 'autocomplete-highlighters', function (Y) {

	  //var titles = [ 'Alabama', 'Alaska', ];
	  var titlestr = Y.one('#titlestr');
	  var titles = titlestr._node.value.split(',');
	Y.one('#title').plug(Y.Plugin.AutoComplete, {
	  resultFilters    : 'phraseMatch',
	  resultHighlighter: 'phraseMatch',
	  source           : titles
    });
});
/*
YUI({filter:'raw'}).use('autocomplete', 'autocomplete-filters', 'autocomplete-highlighters','datasource-get', function (Y) {


	  var titles = [ 'Alabama', 'Alaska', ];
	Y.one('#title').plug(Y.Plugin.AutoComplete, {
	  resultFilters    : 'phraseMatch',
	  resultHighlighter: 'phraseMatch',
	  resultListLocator: 'titles',
	  source           : 'http://localhost:8000/productTitles'
    });
});
*/
/*
YUI().use('autocomplete', 'autocomplete-highlighters', 'datasource-get', function (Y) {
	// Create a DataSource instance.
	var ds = new Y.DataSource.Get({
		//source: 'http://query.yahooapis.com/v1/public/yql?format=json'
		source: 'http://localhost:8000'
	    });

	Y.one('#title').plug(Y.Plugin.AutoComplete, {
		maxResults: 10,
		    resultHighlighter: 'wordMatch',
		    resultTextLocator: 'name',

		    // Use the DataSource instance as the result source.
		    source: ds,

		    // YQL query to use for each request (URL-encoded, except for the
		    // {query} placeholder). This will be appended to the URL that was supplied
		    // to the DataSource's "source" config above.
		    //requestTemplate: '&q=select%20*%20from%20music.artist.search%20where%20keyword%3D%22{query}%22',
		    requestTemplate: '/productTitles/',

		    // Custom result list locator to parse the results out of the YQL response.
		    // This is necessary because YQL sometimes returns an array of results, and
		    // sometimes just a single result that isn't in an array.
		    resultListLocator: function (response) {
		    alert('test');
		    if(response == null){
		    alert('response is null');
		    }
		    else{
		    alert('response is not null');
		    }
		    for ( var prop in response){
			alert ('prop:' +prop+' value ='+response[prop])
		    }
		    //alert(response);
		    //var jsObj = JSON.parse(response);
		    //alert(jsObj);
		    //alert("title str : "+jsObj['titles']);
      var results = response[0].query.results &&
	  response[0].query.results.Artist;

      if (results && !Y.Lang.isArray(results)) {
	  results = [results];
      }

      return results || [];
		}
	    });
    });
    */









YUI({ filter: 'raw' }).use("io-base", "node",
 
    function(Y) {
 
	//Get a reference to the Node that we are using
	//to report results:
	var div = Y.one('#recent-buys ul');
	var user_id = Y.one("#user_id");
	var csrf = Y.one("#csrf");
	var title = Y.one("#title");
	var link = Y.one("#link");
	var image_link = Y.one("#image_link");
	var price = Y.one("#price");
	var day = Y.one("#date_day");
	var month = Y.one("#date_month");
	var year = Y.one("#date_year");
	var dataString = 'user_id='+ user_id +'&csrf='+csrf+'&title='+title+'&link='; 
	dataString += '&link='+link+'&image_link='+image_link+'&price='+price; 
	dataString += '&date_year='+year+'&date_month='+month+'&date_day='+day
 
	//A function handler to use for successful requests:
	var handleSuccess = function(ioId, o){
	    Y.log(arguments);
	    Y.log("The success handler was called.  Id: " + ioId + ".", "info", "example");
 
	    if(o.responseText !== undefined){
		var s = "<li>PHP response: " + o.responseText + "</li>";
		    //div.set("innerHTML", s);
		alert(o.responseText);
	    }
	}
 
	//A function handler to use for failed requests:
	var handleFailure = function(ioId, o){
	    Y.log("The failure handler was called.  Id: " + ioId + ".", "info", "example");
	    if(o.responseText !== undefined){
		var jsObj = JSON.parse(o.responseText);
		alert(o.responseText);
		//div.set("innerHTML", s);
	    }
	}
 
	//Subscribe our handlers to IO's global custom events:
	Y.on('io:success', handleSuccess);
	Y.on('io:failure', handleFailure);
 
	/* Configuration object for POST transaction */
	var cfg = {
	    method: "POST",
	    data: dataString
	};
 
	//The URL of the resource to which we're POSTing data:
	var sUrl = "/addproduct/";
 
	//Handler to make our XHR request when the button is clicked:
	function makeRequest(){
	    alert('clicked : '+cfg.data);
 
 
	    var request = Y.io(sUrl, cfg);
	    Y.log("Initiating request; Id: " + request.id + ".", "info", "example");
 
	}
 
	// Make a request when the button is clicked:
	Y.on("click", makeRequest, "#acompile");
 
	Y.log("As you interact with this example, relevant steps in the process will be logged here.", "info", "example");
    }
);




    $(function() {
	 $("#addprod1").click(function() { 
	    var user_id = $("#user_id").val();
	    var csrf = $("#csrf").val();
	    var title = $("#title").val();
	    var link = $("#link").val();
	    var image_link = $("#image_link").val();
	    var price = $("#price").val();
	    var day = $("#date_day").val();
	    var month = $("#date_month").val();
	    var year = $("#date_year").val();
	    var dataString = 'user_id='+ user_id +'&csrf='+csrf+'&title='+title+'&link='; 
	    dataString += '&link='+link+'&image_link='+image_link+'&price='+price; 
	    dataString += '&date_year='+year+'&date_month='+month+'&date_day='+day
	     $.ajax({
	       type: "POST",
	       url: "/addproduct/",
	       data: dataString,
	       success: function(rdata) {
		var jsObj = JSON.parse(rdata);
		 var s = "";
		for (i in jsObj){
		   prod = jsObj[i];
		   s += "<li>"+prod.title;
		   s += "&nbsp;&nbsp;";
		   s += prod.date;
		   s += "<input value=\"publish\" type=\"submit\" onClick=\'publishIt(&quot;";
		   s += prod.title;
		   s += "&quot;)'/>";
		   s +="</li>";
		}
		    var div = $('#recent-buys ul');
		    div.html(s);
		    $(':input','#myform')
		     .not(':button, :submit, :reset, :hidden')
		      .val('')
		       .removeAttr('checked')
		        .removeAttr('selected');
	       }
	      });
	     return false;
	});
    });
