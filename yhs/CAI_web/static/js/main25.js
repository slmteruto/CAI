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
        if($('#image_section').css('display')=='block') {
            var form_data = new FormData($('#file_form')[0]);

            $.ajax({
                type: 'POST',
                url: '/upload',
                data:form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    if(data=='-1'){
                        $('#jb-wide-contents-type').css('display', 'block');
                        $('#jb-wide-contents-type').css('background-color', 'rgb(20, 20, 22)');
                        $('#pc-type-result-span').html("정상적인 사진을 올려주세요, 인식 오류입니다.");
                    } else {
                        console.log('Success!');
                        $('#jb-wide-contents-type').css('display', 'block');
                        $('#pc-type-result').css('display', 'block');
                        $('.pc-type-result-span').html(data);
                        $('#pc-type-result-span').html(data);
                    }
                },
            });
        } else {
            alert("사진을 먼저 추가해주세요");
        }
    });
});
