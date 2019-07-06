$(function(){
    alert(1);
        $('#search').click(function(){
            var keyword = $('#keyword').val().trim();

            if(keyword == '') {
                alert('关键字不能为空！');
                return false;
            }
            return true;
        })
    })