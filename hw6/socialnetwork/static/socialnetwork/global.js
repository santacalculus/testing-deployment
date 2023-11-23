"use strict"

// Sends a new request to update the to-do list
function loadPosts() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePage(xhr)
        console.log("yes")
    }

    xhr.open("GET", getURL, true)
    console.log("here")
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        let postresponse = response.posts
        updatePosts(postresponse)
        let commentresponse = response.comments
        updateComments(commentresponse)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}


function updatePosts(items) {
    // Removes the old to-do list items
    let list = document.getElementById("id_global")
    console.log(items)
    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        // Builds a new HTML list item for the todo-list
        
        let existingdiv = document.getElementById("id_post_div_" + item.id)
        if (existingdiv != null) {
            continue
        } else {
            let element = document.createElement("div")
            element.id = "id_post_div_" + item.id
            element.classList.add('post-div')
            let postdate = new Date(item.date_time)
            let itemtime = postdate.toLocaleTimeString([], {year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'})

            element.innerHTML = '<i>Post by' + '<a href="otherprofile/' + item.user_id + '" id="id_post_profile_' + item.id + '"' + ' class="post-profile"> ' + item.user_first + ' ' + item.user_last + '</a> -</i>' + 
            '<span id="id_post_text_' + item.id + '" class="post-text"> ' + sanitize(item.text) + ' </span>-' +
            '<span id="id_post_date_time_' + item.id + '" class="date-time"> ' + itemtime.replace(',', ' ') + ' </span>'

            let commentdiv = document.createElement("div")
            commentdiv.id = "post-" + item.id + "-comments-go-here"
            commentdiv.classList.add('comment-div')
            let commentform = document.createElement("div")
            commentform.classList.add('comment-input-box')
            commentform.innerHTML = '<label>Comment: </label>' + '<input type="text" id ="id_comment_input_text_' + item.id + '" ' + 'name="text">' + 
                                    '<button id="id_comment_button_' + item.id + '" ' + ' onclick="addItem(' + item.id + ')">Submit</button>'
    
            // Adds the todo-list item to the HTML list
            list.prepend(commentform)
            list.prepend(commentdiv)
            list.prepend(element)
            
        }
    }
}

function updateComments(items) {
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        let commentdiv = document.getElementById("post-" + item.post_id + "-comments-go-here")
        
        let existingdiv = document.getElementById("id_comment_div_" + item.id)
        if (existingdiv != null) {
            continue
        } else {
            let element = document.createElement("div")
            element.id = "id_comment_div_" + item.id
            element.classList.add('comment-div')
            let postdate = new Date(item.creation_time)
            let itemtime = postdate.toLocaleTimeString([], {year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'})
            

            element.innerHTML = '<i>Comment by' + '<a href="otherprofile/' + item.creator + '" id="id_comment_profile_' + item.id + '"' + 'class="comment-profile"> ' + item.creator_first + ' ' + item.creator_last + '</a> -</i>' + 
            '<span id="id_comment_text_' + item.id + '" class="comment-text"> ' + sanitize(item.text) + ' </span>-' +
            '<span id="id_comment_date_time_' + item.id + '" class="date-time"> ' + itemtime.replace(',', ' ') + ' </span>'
            commentdiv.append(element)

        }
    }
}


function addItem(post_id) {
    let itemTextElement = document.getElementById("id_comment_input_text_" + post_id)
    let itemTextValue   = itemTextElement.value
    console.log(itemTextValue)
    console.log(post_id)

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addItemURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+"&post_id="+ post_id +"&csrfmiddlewaretoken="+getCSRFToken());
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}