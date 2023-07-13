window.addEventListener("load", () => {
    // 滑块
    slider();
    // 登录
    logIn();
    // 注册
    register();
})

// 滑块
function slider() {
    const login = document.querySelector("#login")
    const register = document.querySelector("#register")
    const form_box = document.querySelector('.form-box')
    const register_box = document.querySelector(".register-box")
    const login_box = document.querySelector(".login-box")

    register.addEventListener('click', () => {
        form_box.style.transform = "translateX(80%)"
        login_box.classList.add("hidden")
        register_box.classList.remove("hidden")
    })

    login.addEventListener('click', () => {
        form_box.style.transform = "translateX(0%)"
        register_box.classList.add("hidden")
        login_box.classList.remove("hidden")
    })
}

// 登录
function logIn() {
    function validatePhoneNumber(phoneNumber) {
        // 定义电话号码的正则表达式模式
        var pattern = /^1[3456789]\d{9}$/;
        // 使用正则表达式进行验证
        return pattern.test(phoneNumber);
    }

    function validatePassword(password) {
        // 定义密码的正则表达式模式
        var pattern = /^(?=.*[a-zA-Z]).{6,}$/;
        // 使用正则表达式进行验证
        return pattern.test(password);
    }

    bt2 = document.querySelector(".bt2")
    bt2.addEventListener('click', (e) => {
        const Telephone = document.querySelector('.ipTelephone').value
        const Password = document.querySelector('.ipPassword').value

        if (validatePhoneNumber(Telephone)) {
            if (validatePassword(Password)) {
                bt2.disabled = true;
                console.log(Telephone, Password);
                axios({
                    url: '/jobs/login/',
                    method: 'POST',
                    data: {
                        phone: Telephone,
                        password: Password
                    }
                }).then((result) => {
                    window.location.href = "/jobs/dashboard/"
                    // alert("登录成功")
                }).catch((error) => {
                    alert(error.response.data.msg)
                    if (error.response.data.msg == "用户名或密码错误") {
                        bt2.disabled = false;
                    }
                });
            } else {
                alert("密码至少包含一个英文字符且长度大于6位")
            }
        } else {
            alert("电话号码无效")
        }
    })
}

// 注册
function register() {
    function validateEmail(email) {
        // 定义电子邮箱地址的正则表达式模式
        var pattern = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        // 使用正则表达式进行验证
        return pattern.test(email);
    }

    function validatePhoneNumber(phoneNumber) {
        // 定义电话号码的正则表达式模式
        var pattern = /^1[3456789]\d{9}$/;
        // 使用正则表达式进行验证
        return pattern.test(phoneNumber);
    }

    function validatePassword(password) {
        // 定义密码的正则表达式模式
        var pattern = /^(?=.*[a-zA-Z]).{6,}$/;
        // 使用正则表达式进行验证
        return pattern.test(password);
    }

    const bt1 = document.querySelector(".bt1")
    bt1.addEventListener('click', (e) => {
        const ipemail = document.querySelector('.ipemail').value
        const iptelephone = document.querySelector('.iptelephone').value
        const ippassword1 = document.querySelector('.ippassword1').value
        const ippassword2 = document.querySelector('.ippassword2').value

        console.log(ipemail, iptelephone, ippassword1, ippassword2);
        if (validateEmail(ipemail)) {
            if (validatePhoneNumber(iptelephone)) {
                if (validatePassword(ippassword1)) {
                    if (ippassword1 == ippassword2) {
                        bt1.disabled = true;
                        axios({
                            url: '/jobs/register/',
                            method: 'POST',
                            data: {
                                email: ipemail,
                                phone: iptelephone,
                                password: ippassword2
                            }
                        }).then((result) => {
                            alert(result.data.msg)
                        }).catch((error) => {
                            alert(error.response.data.msg)
                            if (error.response.data.msg == "用户已存在") {
                                bt1.disabled = false;
                            }
                        })
                    } else {
                        alert("两次密码不一致")
                    }
                } else {
                    alert("密码至少包含一个英文字符且长度大于6位")
                }
            } else {
                alert("电话号码无效")
            }
        } else {
            alert("电子邮箱无效")
        }
    })

}