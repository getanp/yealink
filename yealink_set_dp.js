var page = require('webpage').create();
url = "http://192.168.78.31/servlet?p=login&q=loginForm&jumpto=status";

page.viewportSize = { width: 1920, height: 960 };
page.clipRect = { top: 0, left: 0, width: 1920, height: 960 };

page.onConsoleMessage = function(msg) {
    console.log(msg);
};

function onPageReady() {
    var htmlContent = page.evaluate(function () {
        return document.documentElement.outerHTML;
    });

    //console.log(htmlContent);
    page.evaluate(function() {
        var x = document.getElementsByName("formInput");
        document.querySelector("input[name='username']").value = "admin";
        document.querySelector("input[name='pwd']").value = "admin";
        x[0].submit();

    	window.callPhantom({ exit: true });

    });

    phantom.exit();
}

page.onCallback = function(data){
    if (data.exit) {
        page.render('page.png');
        phantom.exit();
    }
};

page.open(url, function (status) {
    setTimeout(function(){
        page.render("page.png");
        phantom.exit();
    }, 1000);
});

/*page.open("http://192.168.78.31/servlet?p=login&q=loginForm&jumpto=status", function(status) {
	console.log(status)
    if ( status === "success" ) {
        page.evaluate(function() {
	      //var x = document.getElementsByName("formInput");
              //document.querySelector("input[name='username']").value = "admin";
              //document.querySelector("input[name='pwd']").value = "admin";
	      //x[0].submit();

	      window.callPhantom({ exit: true });

        });
        window.setTimeout(function () {
          page.render('colorwheel.png');
          phantom.exit();
        }, 5000);
   }
});*/
