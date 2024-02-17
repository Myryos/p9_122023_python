function viewUserNotFollowed() {
    url = "/search_not_followed_user/"
    const inputUsername = document.getElementById('searchUsername').value

    const not_followed_users_list = document.getElementById('notFollowedUsers')

    not_followed_users_list.innerHTML = ''

    users_names = fetch(url + inputUsername).then(response => response.json())
        .then(data => {
            data.forEach(user => {
                const li = document.createElement('li')
                const button = document.createElement('button')

                button.textContent = "FOLLOW"
                button.addEventListener('click', function () {
                    window.location.href = "/follow/" + user.name
                })
                li.textContent = user.name
                li.appendChild(button)
                not_followed_users_list.appendChild(li)
            });

        })
        .catch(error => {
            console.error(error)
        })
}
