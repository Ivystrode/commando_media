var updateForm = document.querySelector(".user-form")
var editbutton = document.querySelector("#editbutton")

function hideUpdateForm() {
    console.log("function")
    console.log(updateForm.style.display)
    if (updateForm.style.display == 'none') {
        updateForm.style.display = 'block'
        editbutton.textContent = 'Cancel'
    } else {
        updateForm.style.display = 'none'
        editbutton.textContent = 'Edit Profile'
    }
}

function goToIdea(id) {
    window.location.href = "/ideas/" + id
}
function goToComment(location, id) {
    window.location.href = location + id
}
function goToMedia(location, id) {
    console.log("go to media")
    window.location.href = location + id
}
function goToAlbum(slug) {
    console.log("go to media")
    window.location.href = '/albums/' + slug
}

console.log("profile js loaded")