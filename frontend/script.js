const cvItems = document.querySelectorAll(".job--cv")
const cvkeskusItems = document.querySelectorAll(".job--cvkeskus")

const allButton = document.querySelector("#allBtn")
const cvButton = document.querySelector("#cvBtn")
const cvkeskusButton = document.querySelector("#cvkeskusBtn")

const body = document.querySelector("body")
const locationSelect = document.querySelector(".location__select")
const locationSelectText = document.querySelector(".location__select-active")
const locationSelectButton = document.querySelector(".location__select-button")
const locationOptions = document.querySelector(".location__options")

const itFilterStatus = document.querySelector(".it_filter__status")

const urlParams = new URLSearchParams(window.location.search)
let isLocationsOpen = false

body.addEventListener("click", handleBodyClick)
locationSelect.addEventListener("click", handleLocationSelectState)

initialLoadSelectLocation()
initialSetITFilterStatus()

function initialSetITFilterStatus() {
    const category = urlParams.get("category")

    if (category == '1') {
        itFilterStatus.classList.add("active")
    }
}

function initialLoadSelectLocation() {
    const locationRegex = /(?<=location=)\d+/
    const locationMatch = window.location.search.match(locationRegex)
    const locationID = locationMatch ? locationMatch[0] : "2"

    for (let i = 0; i < locationOptions.children.length; i++) {
        const option = locationOptions.children[i]

        if (option.dataset.id === locationID) {
            option.className += " active"
            locationSelectText.innerText = option.innerText
        }
    }
}

function handleLocationSelectState() {
    if (isLocationsOpen) {
        isLocationsOpen = false
        locationOptions.className = "location__options"
        locationSelectButton.className = "location__select-button"
    } else {
        isLocationsOpen = true
        locationOptions.className = "location__options open"
        locationSelectButton.className = "location__select-button open"
    }
}

function handleBodyClick(e) {
    if (!isLocationsOpen || e.target.className.includes("location__select")) return

    if (!e.target.className.includes("location__options")) {
        isLocationsOpen = false
        locationOptions.className = "location__options"
        locationSelectButton.className = "location__select-button"
    }
}

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