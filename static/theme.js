function chgTheme() {

    var currentTheme = getPreferredTheme()
    if (currentTheme === 'dark') {
        var currentTheme = 'light'
    } else {
        var currentTheme = 'dark'
    }
    setStoredTheme(currentTheme)    
    setTheme()
}

const getStoredTheme = () => localStorage.getItem('pref_theme')
const setStoredTheme = theme => localStorage.setItem('pref_theme', theme)

const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const setTheme = () => {
    document.documentElement.setAttribute('data-bs-theme', getPreferredTheme())
}

setTheme()