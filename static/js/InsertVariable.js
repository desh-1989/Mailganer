$('.add-var').click(function(){
	CKEDITOR.instances['id_body'].insertText($(this).val());
});