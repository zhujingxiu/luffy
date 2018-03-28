/**
 * Created by admin on 2018/3/28.
 */

$(document).ready(function () {
    var user_list = {
        '13813801380':{
            'nickname':'luffy',
            'password':'luffy',
            'phone':'13813801380'
        }
    };
    localStorage.setItem("members",JSON.stringify(user_list));
    var identity = JSON.parse(localStorage.getItem('member'));
    if(identity.hasOwnProperty('nickname')){
        $('.navbar .navbar-right .logged .name').text(identity.nickname)
        $('.navbar .navbar-right .nologin').hide()
        $('.navbar .navbar-right .logged').show()
    }
});
$('.dialog-btn-close').on('click',function () {
    $('.dialog').hide()
});
$('.btn-login').on('click',function () {
    var block_obj = null;
    $.each($('.box-login-item'),function () {
        if($(this).css('display') == 'block'){
            block_obj = $(this);
        }
    });
    var identity = $(block_obj).find('.identity').val();
    var password = $(block_obj).find('.password').val();
    if(identity == '' || password == ''){
        $(block_obj).find('.err-msg').empty().html('请输入完整登录信息')
    }
    var members = JSON.parse(localStorage.getItem("members"));
    if(members.hasOwnProperty(identity)){
        console.log('hasMatched');
        var _member = members[identity];
        if(!_member.hasOwnProperty('password') || _member['password'] != password){
            $(block_obj).find('.err-msg').empty().html('登录信息错误');
            return false;
        }
        localStorage.setItem('member',JSON.stringify(_member));
        location.reload()
    }else {
        $(block_obj).find('.err-msg').empty().html('登录信息错误');
        return false;
    }
});
$("#loginDialog .tab-box > span").on("click",function(){
    var index=$(this).index();
    $(this).parent().find("span").removeClass('active').eq(index).show().addClass('active');
    $('#loginDialog .box-login-item').hide();

    $('#loginDialog .box-login').find('.'+$(this).data('rel')).show()
});
$('.articles').on('click','.icon-recommend',function (e) {
    $(this).next('.value').addClass('hasrecommend').text(parseInt($(this).next('.value').text())+1);
    $(this).removeClass('icon-recommend').addClass('icon-disrecommend')
});
$('.articles').on('click','.icon-disrecommend',function (e) {
    $(this).next('.value').removeClass('hasrecommend').text(parseInt($(this).next('.value').text())-1);
    $(this).removeClass('icon-disrecommend').addClass('icon-recommend')
});
$('#memberLogout').on('click',function () {
    localStorage.setItem('member',JSON.stringify({}));
    location.reload()
});
var check_login = function () {
    var identity = JSON.parse(localStorage.getItem('member'));
    if(!identity.hasOwnProperty('nickname')){
        $('#loginDialog').show();
        return false;
    }
    return true;
};
$('#pubShare').on('click',function () {
    if(check_login()){
        $('#pubDialog').show()
    }
});
$('.form-list .channel').on('click',function () {
    $.each($('.form-list .channel'),function () {
        $(this).removeClass('active');
    });
    $(this).addClass('active');
    $('.form-list .channel').parent().find('input[name="channel"]').val($(this).data('rel'))
});
$('.form-list .btn-upload').on('click',function () {
    $(this).next('input:file').trigger('click');
});
$('.form-list .btn-reset').on('click',function () {
    $('.form-list').find('input:text,textarea').val('')
});
$('.form-list .btn-publish').on('click',function () {
    var input_link = $('#inputLink').val(),
        input_title = $('#inputTitle').val(),
        input_channel = $('.box-publish input[name="channel"]').val(),
        input_cover = $('.box-publish input[name="cover"]').val(),
        input_summary = $('#inputSummary').val();
    if(input_link == '' || input_title == ''){
        $('.box-publish .err-msg').html('链接和标题必填');
        return false;
    }
    var identity = JSON.parse(localStorage.getItem('member'));
    var _html = '<div class="item">';
    _html += '<div class="cover">';
    _html += '  <img src="images/pic1.jpg"/>';
    _html += '</div>';
    _html += '<div class="detail">';
    _html += '  <div class="summary">';
    _html += '      <a class="title" href="#" target="_blank">'+input_title+'</a>';
    _html += '      <span class="web-source">'+input_link+'</span>';
    _html += '      <a class="tags" href="#"><span class="item-type">'+input_channel+'</span></a>';
    _html += '  </div>';
    if(input_summary.length>0) {
        _html += '  <div class="description">';
        _html += '      <span class="trunks">'+input_summary+'</span>';
        _html += '  </div>';
    }
    _html += '  <div class="info">';
    _html += '      <a class="info-item" href="javascript:;" title="推荐">';
    _html += '          <span class="info-icon icon-recommend"></span><b class="value">0</b>';
    _html += '      </a>';
    _html += '      <a class="info-item" href="javascript:;" title="1秒前">';
    _html += '          <span class="info-icon icon-topic"></span><b class="value">0</b>';
    _html += '      </a>';
    _html += '      <a class="info-item" href="javascript:;" title="加入私藏" style="width: 69px;">';
    _html += '          <span class="info-icon icon-collect"></span><b class="value nostrong">私藏</b>';
    _html += '      </a>';
    _html += '      <a class="info-item" href="javascript:;">';
    _html += '          <span class="source"><img src="images/source2.jpg"></span><b class="value nostrong">'+identity.nickname+'</b>';
    _html += '      </a>';
    _html += '      <span class="info-item">';
    _html += '          <a href="javascript:;"><b class="value nostrong colorange">1秒前</b><i class="into">入热榜</i>';
    _html += '      </span>';
    _html += '  </div>';
    _html += '</div>';
    _html += '</div>';
    $('.main-content .articles').prepend(_html).fadeIn();
    $('#pubDialog').hide();
});

$('.info').on('click','.icon-topic',function () {
    var obj = $(this).parentsUntil('.detail').next('.commets');
    if(obj.css('display')=='none'){
        obj.css('display','block').slideDown('slow');
    }else{
        obj.css('display','none').slideUp('slow');
    }
});

$('.comment-main').on('hover','.items',function () {
    $('.comment-actions').hide()
    $(this).find('.detail-right .comment-actions').show();
})
$('.comment-main .multreplay').on('click',function () {
    var _user = $(this).parentsUntil('.detail-right').prev('.user').find('.name').text()
    $('.reply .reply-text').val('').attr('placeholder','回复@'+_user).focus()
});
$('.reply .reply-text').on('change',function () {
    if($.trim($(this).val()).length>0){
        $('.reply-submit').css('background-color','#0b629c')
    }
})
$('.reply .reply-submit').on('click',function () {
    var text = $(this).parent().prev('.reply-box').find('.reply-text').val();

    if($.trim(text).length<=0){
        $('.reply .reply-text').focus();
        return false
    }
    var identity = JSON.parse(localStorage.getItem('member'));
    var _html = '<li class="items">';
    _html += '<div class="detail-left">';
    _html += '  <a href="#"><img src="images/source3.jpg"></a>';
    _html += '</div>';
    _html += '<div class="detail-right" style="background-color: rgb(246, 246, 246);">';
    _html += '  <div class="user">';
    _html += '      <a class="name" href="#">'+identity.nickname+'</a>';
    _html += '      <span class="text">'+text+'</span>';
    _html += '      <span class="intotime">1秒钟前发布</span>';
    _html += '  </div>';
    _html += '  <div class="comment-actions" style="display: none;">';
    _html += '      <div class="comment-state">';
    _html += '          <a class="ding" href="javascript:;">';
    _html += '              <b>顶</b><span class="ding-num">[0]</span>';
    _html += '          </a>';
    _html += '          <a class="cai" href="javascript:;">';
    _html += '              <b>踩</b><span class="cai-num">[0]</span>';
    _html += '          </a>';
    _html += '          <span class="line-sep">|</span>';
    _html += '          <a class="see-a multreplay" href="javascript:;">回复</a>';
    _html += '      </div>';
    _html += '  </div>';
    _html += '</div>';
    _html += '</li>';
    console.log($(this).parentsUntil('.comment').find('.comment-main'))
    $(this).parentsUntil('.comment').find('.comment-main').prepend(_html)
});
