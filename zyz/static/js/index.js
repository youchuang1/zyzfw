window.onload = function () {
    // 滑块
    // slider();
    // 验证
    // verification();
    // 弹窗
    // popover();
    // 成功弹窗
    // Success_window();
}

// // 滑块
// function slider() {
//     const login = document.querySelector("#login")
//     const register = document.querySelector("#register")
//     const form_box = document.querySelector('.form-box')
//     const register_box = document.querySelector(".register-box")
//     const login_box = document.querySelector(".login-box")

//     register.addEventListener('click', () => {
//         form_box.style.transform = "translateX(80%)"
//         login_box.classList.add("hidden")
//         register_box.classList.remove("hidden")
//     })

//     login.addEventListener('click', () => {
//         form_box.style.transform = "translateX(0%)"
//         register_box.classList.add("hidden")
//         login_box.classList.remove("hidden")
//     })
// }

// // 验证
// function verification() {
//     const form = document.querySelectorAll('.login-box, .register-box');
//     const telephone = document.querySelectorAll('.iptelephone, .ipTelephone');
//     const accountInput = document.querySelector('.iptext');
//     const passwordInputs = document.querySelectorAll('.ippassword1, .ippassword2, .ipPassword');

//     function validateFormInputs(inputs, regex) {
//         inputs.forEach((input) => {
//             input.addEventListener('input', () => {
//                 if (!regex.test(input.value.trim())) {
//                     input.setCustomValidity(input.placeholder + '格式不正确');
//                     // 在这里设置输入不合法时的文字提示
//                 } else {
//                     input.setCustomValidity('');
//                 }
//             });
//         });
//     }

//     function validateAccountInput(accountInput) {
//         accountInput.addEventListener('input', () => {
//             const illegalCharsRegex = /[^a-zA-Z0-9_-]/g;

//             if (accountInput.value.trim().length < 4) {
//                 accountInput.setCustomValidity('账号长度不能少于4个字符');
//                 // 在这里设置输入不合法时的文字提示
//             } else if (illegalCharsRegex.test(accountInput.value)) {
//                 accountInput.setCustomValidity('账号只能包含字母、数字、下划线和减号');
//                 // 在这里设置输入不合法时的文字提示
//             } else {
//                 accountInput.setCustomValidity('');
//             }
//         });
//     }

//     validateFormInputs(telephone, /^1[3-9]\d{9}$/);
//     validateFormInputs(passwordInputs, /^[a-zA-Z0-9_-]{6,16}$/);

//     if (accountInput) {
//         validateAccountInput(accountInput);
//     }

//     form.forEach((formElement) => {
//         const submitButton = formElement.querySelector('button');

//         submitButton.addEventListener('click', (event) => {
//             event.preventDefault();

//             const invalidInputs = formElement.querySelectorAll(':invalid');
//             invalidInputs.forEach((input) => {
//                 input.reportValidity();
//                 // 在这里显示默认的浏览器提示
//             });
//         });
//     });
// }

// // 弹窗
// function popover() {
//     const close = document.querySelector('.close')
//     const Login_and_registration = document.querySelector('.Login_and_registration')
//     const content = document.querySelector('.content')

//     Login_and_registration.addEventListener('click', () => {
//         content.style.display = 'flex'
//     })
//     close.addEventListener('click', () => {
//         content.style.display = 'none'
//     })
// }

// // 成功弹窗
// function Success_window() {
//     const Head_shot = document.querySelector(".Head_shot")
//     const Successful_login = document.querySelector("#Successful_login")
//     const login_interlayer = document.querySelector(".login_interlayer")

//     Head_shot.addEventListener('click', () => {
//         Successful_login.style.display = 'flex'
//         login_interlayer.style.display = 'block'
//     })

//     login_interlayer.addEventListener('click', () => {
//         Successful_login.style.display = 'none'
//         login_interlayer.style.display = 'none'
//     })
// }

// // 视频选项卡
// function Video_TAB() {
//     const arss = document.querySelectorAll('.tad-nav a')
//     for (let i = 0; i < arss.length; i++) {
//         arss[i].addEventListener('click', () => {
//             document.querySelector('.tad-nav .active').classList.remove('active')
//             arss[i].classList.add('active')

//             document.querySelector('.tab-content .active').classList.remove('active')
//             document.querySelector(`.item:nth-child(${i+1})`).classList.add('active')
//         })
//     }
// }

