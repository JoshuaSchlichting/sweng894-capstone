



$("#createUserForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        headers=getJwtHeader(),
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
            localStorage.setItem('jwt', data.access_token);
        }
    });
});
  