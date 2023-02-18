function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function testAddDirectory()
{
    $.ajax({
       type: "POST",
       url: '',
       data: { csrfmiddlewaretoken: getCookie('csrftoken'),
               task: "add_search_directory",
               new_directory: document.getElementById("inputnewdirectory").value},
       success: function callback(response){

                   console.log("Response from JS", response);

        }});

}

