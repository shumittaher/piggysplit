function fetchActiveRoute() {

    let activeroute = location.pathname
    activeroute == "/select" ? activeroute = "/trips":{}
    return (activeroute)
    
}

function updateActiveStatus() {
    
    let links = document.querySelectorAll(".nav-link")
    let activeRoute = fetchActiveRoute()
    
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