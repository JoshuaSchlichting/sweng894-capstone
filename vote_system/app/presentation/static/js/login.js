$("#loginForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data){
            if(data){
                localStorage.setItem('jwt', data.access_token);
                window.location = "/";
            }else{
                alert("An error occurred while logging in!");
            }
        },
        error: function(data){
            alert("Error: " + data.responseJSON.msg);
        }
    });
});
  