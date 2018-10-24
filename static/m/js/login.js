var	form,username,password;
function checkFormData(obj){
	form = $(obj) || $('#loginForm'),
	username = $('#username', form),
	password = $('#password', form);

	if (check(username) && check(password)){
		$.ajax({
			type: "post",
			url: form.attr('action'),
			data:form.serialize(),
			dataType:"jsonp",
			jsonpCallback:'login',
			success: function(data, textStatus){
				//alert(123);
			}
		});
	}
	return false;
}
var timer;
function login(json){
	if(json.msgtype=='error'){
		$('#login_error', form).html(json.content);
	}else if(json.msgtype=='succeed'){
		window.location.href = json.location;
	}else if(json.msgtype=='warning')
        {
            $('#login_error', form).html(json.content);
        }
}
var check = function (input) {
	if (input.val() === ''||input.val() == input.attr('title')) {
		inputError(input);
		input.focus();
		return false;
	} else {
		return true;
	};
};
// 输入错误提示
var inputError = function (input) {
	clearTimeout(inputError.timer);
	var num = 0;
	var fn = function () {
		inputError.timer = setTimeout(function () {
			input.toggleClass('login-form-error');
			if (num === 5) {
				input.removeClass('login-form-error');
			} else {
				fn(num ++);
			};
		}, 150);
	};
	fn();
};


function normalFormAction(){
	$('#loginForm').attr('action','');
}

function initidInputWidth(){
	$('#idInput').width(237-$('#university').outerWidth(true));
}
function checkLogin(form){
	if(form.username.value==''){
		alert('请填写账号名');
		form.username.focus();
		return false;
	}
	if(form.password.value==''){
		alert('请填写密码');
		form.password.focus();
		return false;
	}
	return true;
}
//检测企业登录
$(function(){
	$.ajax({
		type:'post',
		url:'/vip/user/linfo',
		data:{ajax:true},
		dataType:"json",
		beforeSend: function(){
			//loading_black_50.gif
			$('.iSide .loginItem').append('<img id="loadImg" style="margin:30px 0 0 90px;" src="/static/images/loading_black_50.gif" />');
			$('.iSide .loginItem .ic, #mobile, #mobile div:first').hide();
		},
		success: function(data, status){
			$('#loadImg').remove();
			$('.iSide .loginItem .ic, .iSide .loginItem .it, #mobile, #mobile div:first').show();
			if(data.status=='y'){
				$('.iSide .loginItem .it').removeClass('title').addClass('loginTab').show().html('<li class="curr"><a href="#">会员中心</a></li>');
				var h = '<div class="u1"> 欢迎您,<span>'+data.name+'</span> </div> \
					<div class="u2"> \
						<div class="msg"><a href="/vip/largefairs/list">用户中心</a><span></span></div> \
					</div> \
					<div class="u3"> \
						<a href="/vip/home/basicinfo">基本信息</a> \
						<a href="/vip/largefairs/list">展位预定</a> \
						<a href="/vip/user/logout">退出</a> \
					</div>';
					//<a href="/vip/home/jobmanage">职位发布</a> \
				$('.iSide .loginItem .ic').show().addClass('user').html(h);
				$('#mobile').hide();
			}
		}
	});
});
