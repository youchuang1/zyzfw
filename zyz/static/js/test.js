$(document).ready(function () {
    var Page = 1;
    let userList = $('#user-list');
    const perPage = 10;
    // 默认加载第一页
    loadUsers();

    function loadUsers(query = '') {
        $.ajax({
            url: '/jobs/user_list/',
            data: {page: Page, per_page: perPage, query: query},
            dataType: 'json',  // 返回的数据类型
            success: function (response) {

                console.log(response);
                response.data.forEach(function (user) { // 遍历每个用户

                    userList.append('<div>User ID: ' + user.id + ', Username: ' + user.name + ', Email: ' + user.email + '</div>');
                });

                if (!response.isPage) { // 如果已经到最后一页
                    observer.unobserve(bottom); // 取消监听底部元素
                    userList.append('<div>已经到底了</div>');
                }
            }
        });
    }

    // 创建一个滚动条观察者，到底部时加载下一页
    let observer = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
            Page += 1;
            loadUsers();
        }
    }, {threshold: [1]});

    // 监听底部元素
    const bottom = document.querySelector('#bottom');
    observer.observe(bottom);

    // 搜索
    let searchTimeout; // 用于存储 setTimeout 的 ID
    const searchInput = $('#search');
    searchInput.on('input', function () {
        const query = $(this).val().trim();

        clearTimeout(searchTimeout); // 清除上一个 setTimeout
        searchTimeout = setTimeout(function () { // 设置新的 setTimeout
            $('#user-list').empty(); // 清空用户列表
            Page = 1; // 重置页数
            loadUsers(query); // 重新加载用户列表
        }, 500); // 设置间隔为 500 毫秒
    });
});
