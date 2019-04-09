$(function(){
    
    $.fn.filepond.registerPlugin(FilePondPluginFileValidateSize);
    // Turn input element into a pond
    $('.my-pond').filepond();
    
    // Turn input element into a pond with configuration options
    $('.my-pond').filepond({
        allowMultiple: false,
	maxFileSize: '1MB',
	server: {
	    url: './',
	    process: {
		url:'./upload',  // flask data processing app
		headers:{'X-CSRF-TOKEN': $('input[name="csrf_token"]').val()},
		onload: onResponse,
	    },
	  }
    });
    
    $('.form-root').on('FilePond:addfile', function(e) {
        console.log('File added: ', e.detail);
    });
    
    function onResponse(r){
	// create radio button with value of filename right after pond
	r=$.parseJSON(r);
	let filename=r.filename[0];
	console.log('filename by onload: '+filename);
	var $select=$(".file_selection");
	$select.empty(); // clear child elements of $select
	var $input = $('<input type="radio" name="selected_file" value="' + filename +'" /> ').attr("checked", true)
	var $label=$('<label>'+filename+'</label> <br />')
	$select.append($input).append($label);
    }
});

