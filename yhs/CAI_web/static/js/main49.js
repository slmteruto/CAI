var filter = "win16|win32|win64|mac|macintel";
if(navigator.platform){
    if(filter.indexOf(navigator.platform.toLowerCase()) < 0) {
        document.getElementById("cssLink").href="../static/css/main_css1.css";
    } else {
        document.getElementById("cssLink").href="../static/css/main_web7.css";
    }
}

function menu2(){
    if($('#image_section').css('display') == 'block' && $('jb-wide-contents-type').css('background-color') != 'rgb(20, 20, 22)'){
//        location.href = "http://ec2-13-209-69-114.ap-northeast-2.compute.amazonaws.com:8080/color_recommnd"
        if($('#jb-wide-contents-type').css('display')=='block'){
            location.href = "http://13.209.69.114:8080/color_recommnd"
        } else {
            alert("타입보기를 눌러주세요")
        }
    } else {
        alert("사진을 먼저 올려주세요")
    }
}

function menu3(){
    if($('#image_section').css('display') == 'block' && $('jb-wide-contents-type').css('background-color') != 'rgb(20, 20, 22)'){
//        location.href = "http://ec2-13-209-69-114.ap-northeast-2.compute.amazonaws.com:8080/musinsa_recommnd"
        if($('#jb-wide-contents-type').css('display')=='block'){
            location.href = "http://13.209.69.114:8080/musinsa_recommnd"
        } else {
            alert("타입보기를 눌러주세요")
        }

    } else {
        alert("사진을 먼저 올려주세요")
    }

}


function readURL(input){
    if(input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#image_section').css('display', 'block');
            $('#image_section').attr('src', e.target.result);
            $('#image_section').css('height', '600px');
            $('#image_section').css('width', 'auto');
            $('#image_section').css('margin-top', '100px');
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
                dataType:"json",
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    if(data.pctype =='error'){
                        $('#jb-wide-contents-type').css('display', 'block');
                        $('#jb-wide-contents-type').css('background-color', 'rgb(20, 20, 22)');
                        $('#pc-type-result-span').html("정상적인 사진을 올려주세요<br>인식 오류입니다.");
                    } else {
                        var toHex = function( string ){
                            string = parseInt( string, 10 ).toString( 16 );
                            string = ( string.length === 1 ) ? "0" + string : string;
                            return string;
                        };
                        sessionStorage.setItem("rgb_value", data.rgb_value);
                        var r = toHex(data.rgb_value[0]);
                        var g = toHex(data.rgb_value[1]);
                        var b = toHex(data.rgb_value[2]);
                        var hexColor = '#'+r+g+b;
                        console.log(data.rgb_value);
                        console.log('Success!');
                        $('#jb-wide-contents-type').css('display', 'block');
                        $('#pc-type-result').css('display', 'block');
                        $('#jb-wide-contents-type').css('background-color', hexColor);
                        $('.pc-type-result-span').html(data.pctype);
                        $('#pc-type-result-span').html(data.pctype);
                    }
                },
            });
        } else {
            alert("사진을 먼저 추가해주세요");
        }
    });
});
