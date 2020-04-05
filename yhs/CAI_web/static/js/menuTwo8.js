

function bt_male_func(){
    $('#model_m').css('display', 'block');
    $('#model_w').css('display', 'none');
}

function bt_female_func(){
    $('#model_m').css('display', 'none');
    $('#model_w').css('display', 'block');
}

$(function() {
    $('.palette_color').click(function() {
        var rgb_value = $(this).css("background-color").replace('rgb', '').replace(')', '').replace('(', '').split(',');
        console.log(rgb_value);
        var toHex = function( string ){
            string = parseInt( string, 10 ).toString( 16 );
            string = ( string.length === 1 ) ? "0" + string : string;
            return string;
        };

        var r = toHex(rgb_value[0].trim());
        var g = toHex(rgb_value[1].trim());
        var b = toHex(rgb_value[2].trim());
        var hexColor = '#'+r+g+b;
        console.log(hexColor);
        $('#img_bottom_m').css('background-color', hexColor);
        $('#img_bottom_w').css('background-color', hexColor);

    });
});