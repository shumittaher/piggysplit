function setActiveRoute(event) {

    let pathname = event.target.pathname
    if (pathname =="/logout"){
        pathname = "/login"
    }
    localStorage.setItem('currentActiveRoute', pathname)
    
}

function updateActiveStatus() {
    
    let links = document.querySelectorAll(".nav-link")
    let activeRoute = localStorage.getItem('currentActiveRoute')
    
    links.forEach(link => {
        if (link.pathname==activeRoute) {
            link.classList.add("active")
            link.ariaCurrent = "page"
        } else {
            link.classList.remove("active")
            link.removeAttribute("ariaCurrent")
        }
    });
    
}

updateActiveStatus()