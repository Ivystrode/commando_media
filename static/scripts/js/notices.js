var commentform = document.querySelector("#comment-form")
var commentpostbutton = document.querySelector("#comment-post-button")

function showCommentForm(){
    commentpostbutton.style.display = 'none'
    commentform.style.display = 'block'
}

function closeCommentBox(){
    commentpostbutton.style.display = 'block'
    commentform.style.display = 'none'
}

function goToNotice(id) {
    window.location.href = id
}