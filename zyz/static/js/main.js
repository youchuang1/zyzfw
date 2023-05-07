$('.back-to-top').click(function () {
    $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
    return false;
});


$('.sidebar-toggler').click(function () {
    $('.sidebar, .content').toggleClass("open");
    return false;
});

function getInfo() {
    $.ajax({
        url: "/jobs/info/",
        type: "GET",
        success: function (data) {
            console.log(data)
            if (data.code === 0) {
                //将获取到的数据填充到表单中
                $("#area").val(data.data.area);  //地区
                $("#school").val(data.data.school); //学校
                $("#major").val(data.data.major); //专业
                $("#name").val(data.data.name); //名字
                $("#email").val(data.data.email); //邮箱
                $("#name_s").text(data.data.name) //用户名
                $("#jf").text(data.data.score) //积分
                $("#dj").text(data.data.level) //等级
            } else {
                alert(data.message);
            }
        },
        error: function (data) {
            alert("获取用户信息失败");
        }
    });
}

$(document).ready(function () {
    getInfo();
});
$('#info_on').click(function () {
    $.ajax({
        url: "/jobs/info/",
        type: "POST",
        data: {
            'area': $("#area").val(),   //地区
            'school': $("#school").val(),  //学校
            'major': $("#major").val(),  //专业
            'name': $("#name").val(),  //名字
            'email': $("#email").val(),  //邮箱
        },
        success: function (data) {
            if (data.code === 0) {
                //关闭弹窗
                $('#editProfileModal').modal('hide');
            } else {
                alert(data.message);
            }
        },
        error: function (data) {
            alert("修改失败");
        }
    });
});
$('#passwd_on').click(function () {
    if ($("#newPassword").val() != $("#confirmPassword").val()) {
        alert("两次输入的密码不一致");
        return;
    }
    $.ajax({
        url: "/jobs/pwd/",
        type: "POST",
        data: {
            "password": $("#newPassword").val(),
        },
        success: function (data) {
            if (data.code === 0) {
                //清空表单
                $("#newPassword").val("");
                $("#confirmPassword").val("");
                //关闭弹窗
                $('#changePasswordModal').modal('hide');
            } else {
                alert(data.data);
            }
        },
        error: function (data) {
            alert("修改失败");
        }
    });
});