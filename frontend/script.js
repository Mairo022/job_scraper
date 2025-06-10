const locationSelect = document.querySelector(".location__select")
const locationSelectText = document.querySelector(".location__select-active")
const locationSelectButton = document.querySelector(".location__select-button")
const locationOptions = document.querySelector(".location__options")

const itFilterStatus = document.querySelector("#it_filter_status")

const savedButton = document.querySelector("#saved_view_btn")
let isSavedView = false

const urlParams = new URLSearchParams(window.location.search)
let isLocationsOpen = false

document.body.addEventListener("click", handleBodyClick)
locationSelect.addEventListener("click", handleLocationSelectState)
savedButton.addEventListener("click", handleSavedViewButtonClick)

initialLoadSelectLocation()
initialSetITFilterStatus()

assignSavedJobStatus()

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
    // Close location menu on off click
    const isValidLocationSelectCloseClick = isLocationsOpen 
        && !e.target.className.includes("location__select")
        && !e.target.className.includes("location__options")

    if (isValidLocationSelectCloseClick)
        closeOpenLocationSelect(e)

    if (e.target.classList.contains("job__save")) 
        handleSaveButtonClick(e)
}

function closeOpenLocationSelect(e) {
    isLocationsOpen = false
    locationOptions.className = "location__options"
    locationSelectButton.className = "location__select-button"
}

// Handling saved jobs

function getSavedJobs() {
    const savedStr = localStorage.getItem("saved")
    return JSON.parse(savedStr)
}

function handleSaveButtonClick(e) {
    const doUnsave = e.target.classList.contains("saved")
    const savedJobs = getSavedJobs() ?? []

    const ad = e.target.parentElement
    const url = ad.querySelector(".job__position > a").href
    const title = ad.querySelector(".job__position").innerText
    const company = ad.querySelector(".job__info__company").innerText

    if (doUnsave) {
        e.target.classList.remove("saved")
        
        const savedJobsCleaned = savedJobs.filter(job => job?.url != url)
        localStorage.setItem("saved", JSON.stringify(savedJobsCleaned))

        if (savedJobs.length == savedJobsCleaned.length) {
            console.log("Could not find as saved job: ", title)
        }

        updateSavedView()
        assignUnsavedJobStatus()

        return
    }

    e.target.classList.add("saved")

    savedJobs.push({title, company, url, added: new Date()})
    localStorage.setItem("saved", JSON.stringify(savedJobs))

    assignSavedJobStatus()
}

function assignUnsavedJobStatus() {
    const savedJobs = getSavedJobs()
    const jobsUl = document.querySelector(".jobs > ul")

    if (savedJobs.length == 0) {
        for (const job of jobsUl.children) {
            const jobSaveEl = job.querySelector(".job__save")

            if (jobSaveEl.classList.contains("saved")) {
                jobSaveEl.classList.remove("saved")
            }
        }

        return
    }

    for (const job of jobsUl.children) {
        const jobSaveEl = job.querySelector(".job__save")
        const url = job.querySelector(".job__position > a").href
        const isSaved = savedJobs.some(savedJob => savedJob.url === url)

        if (!isSaved && jobSaveEl.classList.contains("saved")) {
            jobSaveEl.classList.remove("saved")
        }
    }   
}

function assignSavedJobStatus() {
    const savedJobs = getSavedJobs()
    if (!savedJobs || savedJobs.length == 0) return

    const jobsUl = document.querySelector(".jobs > ul")
    let assigned = 0

    for (const job of jobsUl.children) {
        const url = job.querySelector(".job__position > a")?.href
        const isSaved = savedJobs.some(savedJob => savedJob.url === url)

        if (isSaved) {
            const jobSaveEl = job.querySelector(".job__save")

            jobSaveEl.classList.add("saved")

            assigned++
        }

        if (assigned == savedJobs.length) return
    }
}

function handleSavedViewButtonClick() {
    if (isSavedView) removeSavedView()
    else createSavedView()

    isSavedView = !isSavedView

    const savedButtonStatus = savedButton.querySelector("#saved_view_status")
    
    if (isSavedView) savedButtonStatus.classList.add("active")
    else savedButtonStatus.classList.remove("active")
}

function updateSavedView() {
    if (!isSavedView) return

    const savedJobsUl = document.querySelector(".jobs__saved")
    savedJobsUl.remove()
    createSavedView()
}

function createSavedView() {
    const jobsSection = document.querySelector(".jobs")
    const ul = document.createElement("ul")
    const savedJobs = getSavedJobs().reverse()
    
    savedJobs.forEach((job) => {
        ul.insertAdjacentHTML('beforeend', `
            <li class="job">
                <h3 class="job__position">
                    <a href="${job.url}">${job.title}</a>
                </h3>
                <div class="job__info">
                    <span class="job__info__company">${job.company}</span>
                    <div class="job__info__details">
                        <span class="job__row__detail">Salvestatud ${formatTime(job.added)}</span>
                    </div>
                </div>
                <div class="job__save saved delete"><svg viewBox="0 0 24 24" height="34px" width="34px" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M20.5001 6H3.5" stroke="#000000" stroke-width="1.5" stroke-linecap="round"></path> <path d="M18.8332 8.5L18.3732 15.3991C18.1962 18.054 18.1077 19.3815 17.2427 20.1907C16.3777 21 15.0473 21 12.3865 21H11.6132C8.95235 21 7.62195 21 6.75694 20.1907C5.89194 19.3815 5.80344 18.054 5.62644 15.3991L5.1665 8.5" stroke="#000000" stroke-width="1.5" stroke-linecap="round"></path> <path d="M6.5 6C6.55588 6 6.58382 6 6.60915 5.99936C7.43259 5.97849 8.15902 5.45491 8.43922 4.68032C8.44784 4.65649 8.45667 4.62999 8.47434 4.57697L8.57143 4.28571C8.65431 4.03708 8.69575 3.91276 8.75071 3.8072C8.97001 3.38607 9.37574 3.09364 9.84461 3.01877C9.96213 3 10.0932 3 10.3553 3H13.6447C13.9068 3 14.0379 3 14.1554 3.01877C14.6243 3.09364 15.03 3.38607 15.2493 3.8072C15.3043 3.91276 15.3457 4.03708 15.4286 4.28571L15.5257 4.57697C15.5433 4.62992 15.5522 4.65651 15.5608 4.68032C15.841 5.45491 16.5674 5.97849 17.3909 5.99936C17.4162 6 17.4441 6 17.5 6" stroke="#000000" stroke-width="1.5"></path> </g></svg></div>
            </li>
        `)
    })

    const jobsUl = document.querySelector(".jobs > ul")
    const paging = document.querySelector(".jobs__paging")

    if (jobsUl) jobsUl.style.display = "none"
    if (paging) paging.style.display = "none"

    ul.className = "jobs__saved"
    jobsSection.appendChild(ul)
}

function removeSavedView() {
    const jobsUl = document.querySelector(".jobs > ul")
    const paging = document.querySelector(".jobs__paging")

    if (jobsUl) jobsUl.style.display = "block"
    if (paging) paging.style.display = "block"

    const savedJobsUl = document.querySelector(".jobs__saved")
    savedJobsUl.remove()
}

function formatTime(timeInputStr) {
    const timeInput = new Date(timeInputStr);
    const timeNow = new Date();
    const timeDiff = new Date(timeNow - timeInput);

    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    const hours = timeDiff.getUTCHours();
    const minutes = timeDiff.getUTCMinutes();
    const seconds = timeDiff.getUTCSeconds();

    if (days > 0) {
        if (days === 1) return "Päev tagasi";
        if (days < 7) return `${days} p. tagasi`;
        if (days < 14) return "Nädal tagasi";

        return Math.round(days / 7) + " näd. tagasi";
    }

    if (hours > 0) return hours === 1 ? "Tund tagasi" : `${hours} tundi tagasi`;
    if (minutes > 0) return minutes === 0 ? "Minut tagasi" : `${minutes} min. tagasi`;
    if (seconds > 0) return `${seconds} s. tagasi`;

    return "1 s. tagasi"
}
