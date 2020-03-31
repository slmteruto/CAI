function typeSubmit(){
    if(document.getElementById("ex_file".value == "")){
        alert("???");
    } else {
        document.getElementById("file_form").submit();
    }
}

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


$(function(){
    $("#show_type").click(function(){
        var form = $('form')[0];
        var formData = new FormData(form);
            $.ajax({
                url:'/upload',
                processData : false,
                contentType : false,
                data : formData,
                type : 'POST',
                success : function(result){
                    alert("ajax테스트");
                }
            });
    });
});