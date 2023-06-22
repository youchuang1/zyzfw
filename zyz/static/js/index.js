$(document).ready(function () {
    // 滑块
    slider();
    // 验证
    verification();
    // 弹窗
    popover();
    // 成功弹窗
    Success_window();
    // 视频选项卡
    Video_TAB();
});

// 滑块
function slider() {
    const login = $("#login");
    const register = $("#register");
    const form_box = $(".form-box");
    const register_box = $(".register-box");
    const login_box = $(".login-box");

    register.on("click", () => {
        //清空表单
        $(".register-box input").val("");
        form_box.css("transform", "translateX(80%)");
        login_box.addClass("hidden");
        register_box.removeClass("hidden");
    });

    login.on("click", () => {
        //清空表单
        $(".login-box input").val("");
        form_box.css("transform", "translateX(0%)");
        register_box.addClass("hidden");
        login_box.removeClass("hidden");
    });
}

// 验证
function verification() {
    const form = $(".login-box, .register-box");
    const telephone = $(".iptelephone, .ipTelephone");
    const accountInput = $(".iptext");
    const passwordInputs = $(".ippassword1, .ippassword2, .ipPassword");

    function validateFormInputs(inputs, regex) {
        inputs.on("input", function () {
            const input = $(this);

            if (!regex.test(input.val().trim())) {
                input[0].setCustomValidity(input.attr("placeholder") + "格式不正确");
            } else {
                input[0].setCustomValidity("");
            }
        });
    }

    function validateAccountInput(accountInput) {
        accountInput.on("input", function () {
            const illegalCharsRegex = /[^a-zA-Z0-9_-]/g;

            if (accountInput.val().trim().length < 4) {
                accountInput[0].setCustomValidity("账号长度不能少于4个字符");
            } else if (illegalCharsRegex.test(accountInput.val())) {
                accountInput[0].setCustomValidity("账号只能包含字母、数字、下划线和减号");
            } else {
                accountInput[0].setCustomValidity("");
            }
        });
    }

    validateFormInputs(telephone, /^1[3-9]\d{9}$/);
    validateFormInputs(passwordInputs, /^[a-zA-Z0-9_-]{6,16}$/);

    if (accountInput.length) {
        validateAccountInput(accountInput);
    }

    form.each(function () {
        const formElement = $(this);
        const submitButton = formElement.find("button");

        submitButton.on("click", function (event) {
            event.preventDefault();

            const invalidInputs = formElement.find(":invalid");
            invalidInputs.each(function () {
                this.reportValidity();
            });
        });
    });
}

// 弹窗
function popover() {
    const close = $(".close");
    const Login_and_registration = $(".Login_and_registration");
    const content = $(".content");

    Login_and_registration.on("click", () => {
        content.css("display", "flex");
    });

    close.on("click", () => {
        content.css("display", "none");
    });
}

// 成功弹窗
function Success_window() {
    const Head_shot = $(".Head_shot");
    const Successful_login = $("#Successful_login");
    const login_interlayer = $(".login_interlayer");

    Head_shot.on("click", () => {
        Successful_login.css("display", "flex");
        login_interlayer.css("display", "block");
    });

    login_interlayer.on("click", () => {
        Successful_login.css("display", "none");
        login_interlayer.css("display", "none");
    });
}

// 视频选项卡
function Video_TAB() {
    const arss = $(".tad-nav a");
    arss.each(function (index) {
        $(this).on("click", function () {
            $(".tad-nav .active").removeClass("active");
            $(this).addClass("active");

            $(".tab-content .active").removeClass("active");
            $(`.item:nth-child(${index + 1})`).addClass("active");
        });
    });
}

$(document).on("click", "#login-btn", function () {
    const phone = $("#phone_dl").val();
    const password = $("#password_dl").val();

    if (!phone || !password) {
        alert("请填写完整的登录信息");
        return;
    }

    $.ajax({
        url: "/jobs/login/",
        type: "POST",
        data: {
            phone: phone,
            password: password
        },
        success: function (data) {
            if (data.code === 0) {
                window.location.href = "/jobs/dashboard/";
            } else {
                // $("#error-message").show();
                alert("登录失败：")
            }
        }
    });
});

$(document).on("click", "#register-btn", function () {
    const phone = $("#phone_zc").val();
    const email = $("#email").val();
    const password = $("#password_zc").val();
    const password2 = $("#password2_zc").val();

    if (!phone || !email || !password) {
        alert("请填写完整的注册信息");
        return;
    } else if (password !== password2) {
        alert("两次输入的密码不一致");
        return;
    }

    $.ajax({
        url: "/jobs/register/",
        method: "POST",
        data: {
            phone: phone,
            email: email,
            password: password
        },
        success: function (response) {
            if (response.code === 0) {
                alert("注册成功");
                //关闭注册框
                $(".close").click();
            } else {
                alert("注册失败：" + response.msg);
            }
        },
        error: function () {
            alert("请求失败，请稍后重试");
        }
    });
});