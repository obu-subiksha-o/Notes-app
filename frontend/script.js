const API_URL = "https://notes-app-5aut.onrender.com"

let token = ""
let currentNoteId = null

let myNotes = []
let sharedNotes = []

function showRegister() {
    loginPage.classList.add("hidden")
    registerPage.classList.remove("hidden")
}

function showLogin() {
    registerPage.classList.add("hidden")
    loginPage.classList.remove("hidden")
}

async function register() {

    const email = registerEmail.value
    const password = registerPassword.value

    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    })

    const data = await response.json()

    if(response.ok){
        await autoLogin(email,password)
    } else {
        alert(data.detail)
    }
}

async function autoLogin(email,password){

    const response = await fetch(`${API_URL}/login`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            email,
            password
        })
    })

    const data = await response.json()

    token = data.access_token

    openDashboard()
}

async function login(){

    const email = loginEmail.value
    const password = loginPassword.value

    const response = await fetch(`${API_URL}/login`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            email,
            password
        })
    })

    const data = await response.json()

    if(response.ok){

        token = data.access_token

        openDashboard()

    } else {

        alert(data.detail)
    }
}

function openDashboard(){

    loginPage.classList.add("hidden")
    registerPage.classList.add("hidden")

    dashboard.classList.remove("hidden")

    loadNotes()
    loadNotifications()
}

async function loadNotes(){

    const response = await fetch(`${API_URL}/notes`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })

    const data = await response.json()

    myNotes = data.my_notes || []
    sharedNotes = data.shared_notes || []

    renderMyNotes()
    renderSharedNotes()
}

function renderMyNotes(){

    myNotesList.innerHTML = ""

    myNotes.forEach(note=>{
        myNotesList.innerHTML += createNote(note)
    })
}

function renderSharedNotes(){

    sharedNotesList.innerHTML = ""

    sharedNotes.forEach(note=>{

        sharedNotesList.innerHTML += `

        <div class="note-item"
            onclick="openNote(
                ${note.id},
                \`${note.title}\`,
                \`${note.content}\`
            )">

            <h3>
                <i class="fa-solid fa-share-nodes"></i>
                ${note.title}
            </h3>

            <p>Shared with you</p>

        </div>
        `
    })
}

function createNote(note){

    return `

    <div class="note-item
        ${currentNoteId === note.id ? "active" : ""}
    "

    onclick="openNote(
        ${note.id},
        \`${note.title}\`,
        \`${note.content}\`
    )">

        <div class="dots-menu"
            onclick="toggleDropdown(event,${note.id})">

            <i class="fa-solid fa-ellipsis"></i>

        </div>

        <div class="dropdown"
            id="dropdown-${note.id}">

            <button onclick="deleteNote(${note.id})">
                Delete
            </button>

        </div>

        <h3>${note.title}</h3>

        <p>${note.content.substring(0,50)}...</p>

    </div>
    `
}

function toggleDropdown(event,id){

    event.stopPropagation()

    document.querySelectorAll(".dropdown")
        .forEach(drop=>{
            drop.style.display = "none"
        })

    const menu =
        document.getElementById(`dropdown-${id}`)

    menu.style.display =
        menu.style.display === "block"
        ? "none"
        : "block"
}

function openNote(id,title,content){

    currentNoteId = id

    noteTitle.value = title
    noteContent.value = content

    renderMyNotes()
}

function newNote(){

    currentNoteId = null

    noteTitle.value = ""
    noteContent.value = ""
}

async function saveNote(){

    const title = noteTitle.value
    const content = noteContent.value

    if(!title || !content){
        alert("Fill all fields")
        return
    }

    const duplicate = myNotes.find(note=>
        note.title === title &&
        note.content === content &&
        note.id !== currentNoteId
    )

    if(duplicate){
        alert("Duplicate note exists")
        return
    }

    if(currentNoteId){

        await fetch(`${API_URL}/notes/${currentNoteId}`,{
            method:"PUT",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${token}`
            },
            body:JSON.stringify({
                title,
                content
            })
        })

    } else {

        await fetch(`${API_URL}/notes`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${token}`
            },
            body:JSON.stringify({
                title,
                content
            })
        })
    }

    loadNotes()

    alert("Saved")
}

async function deleteNote(id){

    event.stopPropagation()

    await fetch(`${API_URL}/notes/${id}`,{
        method:"DELETE",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })

    loadNotes()
}

async function shareNote(){

    if(!currentNoteId){
        alert("Open note first")
        return
    }

    const email = prompt("Enter email")

    if(!email) return

    const response = await fetch(
        `${API_URL}/notes/${currentNoteId}/share`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${token}`
            },
            body:JSON.stringify({
                share_with_email:email
            })
        }
    )

    const data = await response.json()

    alert(data.message)
}

function filterNotes(){

    const value =
        searchInput.value.toLowerCase()

    const filtered =
        myNotes.filter(note=>
            note.title.toLowerCase()
            .includes(value)
        )

    myNotesList.innerHTML = ""

    filtered.forEach(note=>{
        myNotesList.innerHTML += createNote(note)
    })
}

async function loadNotifications(){

    const response = await fetch(
        `${API_URL}/notifications`,
        {
            headers:{
                "Authorization":`Bearer ${token}`
            }
        }
    )

    const data = await response.json()

    if(data.length > 0){

        notificationBadge.classList.remove("hidden")
        notificationBadge.innerText = data.length

    } else {

        notificationBadge.classList.add("hidden")
    }
}

async function openNotifications(){

    dashboard.classList.add("hidden")

    notificationsPage.classList.remove("hidden")

    const response = await fetch(
        `${API_URL}/notifications`,
        {
            headers:{
                "Authorization":`Bearer ${token}`
            }
        }
    )

    const data = await response.json()

    notificationsList.innerHTML = ""

    data.forEach(notification=>{

        notificationsList.innerHTML += `

        <div class="notification-card">

            <h3>
                <i class="fa-regular fa-bell"></i>
                Shared Note
            </h3>

            <p>${notification.message}</p>

        </div>
        `
    })

    await fetch(`${API_URL}/notifications/read`,{
        method:"POST",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })

    notificationBadge.classList.add("hidden")
}

function closeNotifications(){

    notificationsPage.classList.add("hidden")

    dashboard.classList.remove("hidden")
}

function logout(){

    token = ""

    dashboard.classList.add("hidden")

    loginPage.classList.remove("hidden")
}

function toggleTheme(){

    document.body.classList.toggle("dark")
}