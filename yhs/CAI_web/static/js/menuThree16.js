$(function(){
    $('#bt_select').click(function() {
        var nick =$('#input_nick').val();
        console.log(nick);
        $.ajax({
            type: 'POST',
            url: '/selectnick',
            data:{input_nick:nick},
            dataType:"json",
            success: function(data) {
                var bright = data.bright;
                var harmony = data.harmony;
                var purchase = data.purchase;
                console.log(bright);
                console.log(harmony);
                console.log(purchase);
                $('.contents-bright').css('display', 'block');
                $('#brt_rcmd1').css('background-image', 'url("'+bright[0]+'")');
                $('#brt_rcmd2').css('background-image', 'url("'+bright[1]+'")');
                $('#brt_rcmd3').css('background-image', 'url("'+bright[2]+'")');
                $('#brt_rcmd4').css('background-image', 'url("'+bright[3]+'")');
                $('#brt_rcmd5').css('background-image', 'url("'+bright[4]+'")');
                $('#brt_rcmd6').css('background-image', 'url("'+bright[5]+'")');

                $('.contents-harmony').css('display', 'block');
                $('#hrmn_rcmd1').css('background-image', 'url("'+harmony[0]+'")');
                $('#hrmn_rcmd2').css('background-image', 'url("'+harmony[1]+'")');
                $('#hrmn_rcmd3').css('background-image', 'url("'+harmony[2]+'")');
                $('#hrmn_rcmd4').css('background-image', 'url("'+harmony[3]+'")');
                $('#hrmn_rcmd5').css('background-image', 'url("'+harmony[4]+'")');
                $('#hrmn_rcmd6').css('background-image', 'url("'+harmony[5]+'")');



                $('.contents-palette').css('display', 'block');
                $('#pur_rcmd1').css('background-image', 'url("'+purchase[0]+'")');
                $('#pur_rcmd2').css('background-image', 'url("'+purchase[1]+'")');
                $('#pur_rcmd3').css('background-image', 'url("'+purchase[2]+'")');
                $('#pur_rcmd4').css('background-image', 'url("'+purchase[3]+'")');
                $('#pur_rcmd5').css('background-image', 'url("'+purchase[4]+'")');
                $('#pur_rcmd6').css('background-image', 'url("'+purchase[5]+'")');

            },
        });
    });
});


$(function() {
    $('.recommend_prdt').click(function() {
        var img_link = $(this).css("background-image").replace('url("', '').replace('")', '');
        var tmp_link = img_link.replace("https://image.msscdn.net/images/goods_img/", '').split('/');
        var prdt_link = "https://store.musinsa.com/app/product/detail/"+tmp_link[1]
        console.log(prdt_link)
        window.open(prdt_link, "_blank");
    });
});