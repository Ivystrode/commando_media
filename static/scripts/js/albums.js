var album_item_container = document.querySelectorAll('.album_item_container')
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

function goToAlbum(slug) {
    window.location.href = slug
}
function goToPicture(url) {
    window.location.href = url
}

