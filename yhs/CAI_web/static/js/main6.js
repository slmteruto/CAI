//function typeSubmit(){
//    if(document.getElementById("ex_file".value == "")){
//        alert("???");
//    } else {
//        document.getElementById("file_form").submit();
//
//    }
//}

function readURL(input){
    if(input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#image_section').css('display', 'block');
            $('#image_section').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$(function() {
    $('#show_type').click(function() {
        var form_data = new FormData($('#file_form')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
                $('#jb-wide-contents-type').css('display', 'block');
                $('#pc-type-result').css('display', 'block');
            },
        });
    });
});
