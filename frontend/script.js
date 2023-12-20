const cvItems = document.querySelectorAll(".job--cv")
const cvkeskusItems = document.querySelectorAll(".job--cvkeskus")

const allButton = document.querySelector("#allBtn")
const cvButton = document.querySelector("#cvBtn")
const cvkeskusButton = document.querySelector("#cvkeskusBtn")

function navBtnClick(type) {
    if (type === "all") {
        if (allButton.classList.contains("active")) {
            return
        }

        allButton.classList.add("active")
        cvButton.classList.remove("active")
        cvkeskusButton.classList.remove("active")

        styliseJobItemsDisplay("block", "block")
    }

    if (type === "cv") {
        if (cvButton.classList.contains("active")) {
            return
        }

        allButton.classList.remove("active")
        cvButton.classList.add("active")
        cvkeskusButton.classList.remove("active")

        styliseJobItemsDisplay("block", "none")
    }

    if (type === "cvkeskus") {
        if (cvkeskusButton.classList.contains("active")) {
            return
        }

        allButton.classList.remove("active")
        cvButton.classList.remove("active")
        cvkeskusButton.classList.add("active")

        styliseJobItemsDisplay("none", "block")
    }
}

function styliseJobItemsDisplay(cvStyle, cvKeskusStyle) {
    for (let i = 0; i < cvItems.length; i++) {
        cvItems[i].style.display = cvStyle
    }
    for (let i = 0; i < cvkeskusItems.length; i++) {
        cvkeskusItems[i].style.display = cvKeskusStyle
    }
}