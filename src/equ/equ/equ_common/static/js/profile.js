$(document).ready(function(e) {
  $('#id_terms').attr('required',true);
  $('#id_image').change(function() {
    var file = window.URL.createObjectURL(this.files[0]);
    $('#user-pic').attr('src',file);
  });
  $('#user_profile_form').submit(function(e) {
    var checked_cats = [];
    $('#user_categories input[type="checkbox"]:checked').each(function() {
      checked_cats.push($(this).val());
    });
    
    if(checked_cats.length > 0)
      $('#user_cats').val(checked_cats);
    else {
      $(this).find('.btn-space').before('<div style="margin:auto;width:520px;"><div class="alert alert-danger"><strong>Error!</strong> Please select at least one interest.</div></div>');
      e.preventDefault();
    }
  });
});