function callBot() {
  $.ajax({
        type: "POST",
        url: "/app.py",
        data: { param: input },
        success: callbackFunc
    });
}

function callbackFunc(response) {
    // do something with the response
    console.log(response);
	document.write("working");
}