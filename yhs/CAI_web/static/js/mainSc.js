alert('testestest');
function typeSubmit(){
    alert("클릭은됨?")
    if(document.getElementById("ex_file".value == "")){
        alert("");
    } else {
        document.img_type_submit.submit();
    }
}

function readURL(input){
    if(input.files && input.files[0] {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#image_section').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$("#imgInput").change(function(){
    readURL(this);
});