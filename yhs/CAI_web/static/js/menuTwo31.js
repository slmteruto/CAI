var rgb_value = sessionStorage.getItem("rgb_value").split(',');

var toHex = function( string ){
    string = parseInt( string, 10 ).toString( 16 );
    string = ( string.length === 1 ) ? "0" + string : string;
    return string;
};


var bright = data['bright'];
var harmony = data['harmony'];

//console.log(bright[0]);
//console.log(harmony[0]);
$(function(){
    for(var i=0; i<bright.length+1;i++){
        var r = toHex(bright[i][0]);
        var g = toHex(bright[i][1]);
        var b = toHex(bright[i][2]);
        var hexColor_bottom = '#'+r+g+b;
        var clss_name = ".brt-blc"+i;
        $(clss_name).css('background-color', hexColor_bottom);
        $(clss_name+' font').html('RGB</br>'+bright[i][0].toFixed(0)+", "+bright[i][1].toFixed(0)+", "+bright[i][2].toFixed(0));
    }

    for(var i=0; i<harmony.length+1;i++){
        var r = toHex(harmony[i][0]);
        var g = toHex(harmony[i][1]);
        var b = toHex(harmony[i][2]);
        var hexColor_bottom = '#'+r+g+b;
        var clss_name = ".hmny-blc"+i;
        $(clss_name).css('background-color', hexColor_bottom);
        $(clss_name+' font').html('RGB</br>'+harmony[i][0].toFixed(0)+", "+harmony[i][1].toFixed(0)+", "+harmony[i][2].toFixed(0));
    }
});



if(rgb_value != null){
    console.log(rgb_value)
    console.log(rgb_value[0], rgb_value[1], rgb_value[2])
    var r = toHex(rgb_value[0]);
    var g = toHex(rgb_value[1]);
    var b = toHex(rgb_value[2]);
    var hexColor_top = '#'+r+g+b;
    console.log(hexColor_top)

} else {
    var hexColor_top = '#f5d7c8'
}


function bt_male_func(){
    $('#model_m').css('display', 'block');
    $('#model_w').css('display', 'none');
    $('#img_top_m').css('background-color', hexColor_top);
}

function bt_female_func(){
    $('#model_m').css('display', 'none');
    $('#model_w').css('display', 'block');
    $('#img_top_w').css('background-color', hexColor_top);
}


$(function() {
    $('.palette_color').click(function() {
        var rgb_value = $(this).css("background-color").replace('rgb', '').replace(')', '').replace('(', '').split(',');
        console.log(rgb_value);
        var r = toHex(rgb_value[0].trim());
        var g = toHex(rgb_value[1].trim());
        var b = toHex(rgb_value[2].trim());
        var hexColor = '#'+r+g+b;
        console.log(hexColor);
        $('#img_bottom_m').css('background-color', hexColor);
        $('#img_bottom_w').css('background-color', hexColor);

    });
});