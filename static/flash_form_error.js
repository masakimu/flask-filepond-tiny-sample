var tab_attr=""
$("input").each(function(index, elem) {
    elem.addEventListener("invalid", function(e) {
	if (tab_attr == ""){
	    if(e.target.hasAttribute("tab")){
		tab_attr = e.target.attributes["tab"].value;
	    }
	    message = "invalid input; see " + tab_attr + "(" + e.target.id +") @" + e.target.closest('p[class^="paragraph"]').id;
	}
	document.getElementById("form_error_message").innerText = message;
    });
});
