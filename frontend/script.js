const locationSelect = document.querySelector(".location__select")
const locationSelectText = document.querySelector(".location__select-active")
const locationSelectButton = document.querySelector(".location__select-button")
const locationOptions = document.querySelector(".location__options")

const itFilterStatus = document.querySelector(".it_filter__status")

const savedButton = document.querySelector(".saved_filter") 
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
        e.target.innerText = "Salvesta"
        
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
    e.target.innerText = "Salvestatud"

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
                jobSaveEl.innerText = "Salvesta"
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
            jobSaveEl.innerText = "Salvesta"
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
            jobSaveEl.innerText = "Salvestatud"

            assigned++
        }

        if (assigned == savedJobs.length) return
    }
}

function handleSavedViewButtonClick() {
    if (isSavedView) removeSavedView()
    else createSavedView()

    isSavedView = !isSavedView

    const savedButtonStatus = savedButton.querySelector(".saved_filter__status")
    
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
                <div class="job__save saved">Eemalda</div>
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
