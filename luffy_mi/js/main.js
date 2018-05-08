/**
 * Created by admin on 2018/5/8.
 */
$(document).ready(function () {
    $('#filterText').on({
        'focus': function () {
            $(this).parent('form').removeClass('filter-form-focus').addClass('filter-form-focus').find('.hot-words').hide().next('.keyword-list').show();
        },
        'focusout':function () {
            $(this).parent('form').removeClass('filter-form-focus').find('.hot-words').show().next('.keyword-list').hide();
        }
    });
    $('.home-menu .category-list > li').on({
        'mouseover': function () {
            $(this).removeClass('category-item-active').addClass('category-item-active');
        },
        'mouseout': function () {
            $(this).removeClass('category-item-active');
        }
    });
    $('.header-nav .nav-list > li').on({
        'mouseover':function () {
            $(this).removeClass('nav-item-active').addClass('nav-item-active').find('.item-children').show();
        },
        'mouseout': function () {
            $(this).removeClass('nav-item-active').find('.item-children').hide();
        }
    });
    $('.section li.brick-item').on({
        'mouseover': function () {
            $(this).removeClass('brick-item-active').addClass('brick-item-active');
        },
        'mouseout': function () {
            $(this).removeClass('brick-item-active');
        }
    });

    $(".tab-list > li").on("mouseover",function(){
        var index=$(this).index();
        var target=$(this).parent().data('tab-target');
        $(this).parent().find('li').removeClass('tab-active').eq(index).addClass('tab-active');
        $('#'+target).find(".tab-content").removeClass('tab-content-active').hide().eq(index).addClass('tab-content-active').show();
    });
    $('.category-menu > .home-silder').bxSlider({
        auto: true,
        slideWidth: 1226,
        infiniteLoop: true,
        hideControlOnEnd: true,
        slideMargin: 10
    });
    $('.for-recommend > .goods-list').bxSlider({
        slideWidth: 1226,
        minSlides: 5,
        maxSlides: 5,
        slideMargin: 14,
        prevText:'<i class="iconfont icon-prevpage"></i>',
        nextText:'<i class="iconfont icon-nextpage"></i>',
        nextSelector:$('#recommend .control-next'),
        prevSelector:$('#recommend .control-prev'),
        pager: null
    });
    $('.content-item-book .item-list').bxSlider({
        slideWidth: 296,
        infiniteLoop: true,
        prevText:'<i class="iconfont icon-shangyiye"></i>',
        nextText:'<i class="iconfont icon-xiayiye"></i>',
        nextSelector:$('.content-item-book .control-next'),
        prevSelector:$('.content-item-book .control-prev'),
        pagerSelector:$('.content-item-book .pagers-wrapper')
    });
    $('.content-item-theme .item-list').bxSlider({
        slideWidth: 296,
        infiniteLoop: true,
        prevText:'<i class="iconfont icon-shangyiye"></i>',
        nextText:'<i class="iconfont icon-xiayiye"></i>',
        nextSelector:$('.content-item-theme .control-next'),
        prevSelector:$('.content-item-theme .control-prev'),
        pagerSelector:$('.content-item-theme .pagers-wrapper')
    });
    $('.content-item-game .item-list').bxSlider({
        slideWidth: 296,
        infiniteLoop: true,
        prevText:'<i class="iconfont icon-shangyiye"></i>',
        nextText:'<i class="iconfont icon-xiayiye"></i>',
        nextSelector:$('.content-item-game .control-next'),
        prevSelector:$('.content-item-game .control-prev'),
        pagerSelector:$('.content-item-game .pagers-wrapper')
    });
    $('.content-item-app .item-list').bxSlider({
        slideWidth: 296,
        infiniteLoop: true,
        prevText:'<i class="iconfont icon-shangyiye"></i>',
        nextText:'<i class="iconfont icon-xiayiye"></i>',
        nextSelector:$('.content-item-app .control-next'),
        prevSelector:$('.content-item-app .control-prev'),
        pagerSelector:$('.content-item-app .pagers-wrapper')
    });
    $(".play-video").on("click", function(e) {
        e.preventDefault();
        $("#modalVideo").find(".modal-head .title").text($(this).attr("data-video-title")).end().find(".modal-body").html(
            '<iframe id="miPlayerIframe" width="880" height="536" src="//hd.mi.com/f/zt/hd/miplayer2/index.html?vurl=' + $(this).attr("data-video") + "&poster=" + $(this).attr("data-video-poster") + '" frameborder="0" allowfullscreen></iframe>'
        ).find("iframe").focus();
        $("#modalVideo").modal({
            show: !0,
            backdrop: "static"
        })
    });
    $("#modalVideo .close").on("click", function(e) {
        e.preventDefault();
        $("#modalVideo").find(".modal-head .title").empty();
        $("#modalVideo").find(".modal-body").empty();
    });
});