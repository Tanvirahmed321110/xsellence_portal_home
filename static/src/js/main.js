



const sidebar = document.getElementById('sidebar');
function openSidebarDesktop() {
    const collaps_btn = document.getElementById('collaps-btn');
    const main_content = document.querySelector('.main-content');
    const notic_board = document.getElementById('notic-board');

    // ✅ validation (important)
    if (!collaps_btn || !main_content || !sidebar || !notic_board) {
        console.log("Sidebar elements not found ❌");
        return;
    }

    collaps_btn.addEventListener('click', function () {
        sidebar.classList.toggle('sidebar-small');
        main_content.classList.toggle('main-content-big');
        notic_board.classList.toggle('big');
    });
}

openSidebarDesktop()


function mobileSidebar() {
    const mobile_menu_btn = document.getElementById('mobile-menu-btn')
    const menuIcon = document.getElementById('menu-icon');

    if (!mobile_menu_btn || !menuIcon) {
        console.log("Sidebar elements not found ❌");
        return;
    }

    let isOpen = false;

    // icons
    const hamburger = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <line x1="3" y1="7" x2="21" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <line x1="7" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <line x1="11" y1="17" x2="21" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>`;

    const closeIcon = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <line x1="5" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <line x1="19" y1="5" x2="5" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>`;

    menuIcon.innerHTML = hamburger;

    mobile_menu_btn.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        isOpen = !isOpen;

        menuIcon.innerHTML = isOpen ? closeIcon : hamburger;
    });
}

mobileSidebar()


const toggle = document.getElementById("themeToggle");

toggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");

    if (currentTheme === "dark") {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    } else {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
    }
});


document.querySelectorAll('input[type="date"]').forEach(function (input) {
    // Page load এ check
    toggleDateColor(input);

    // Value change হলে check
    input.addEventListener('change', function () {
        toggleDateColor(this);
    });
});


function toggleDateColor(input) {
    if (input.value) {
        input.style.color = 'var(--color-text-header)';
        input.style.fontWeight = '500'
    } else {
        input.style.color = 'var(--color-text-placeholder)';
    }
}









// For List and Grid View
function setView(type) {
    // Panels
    document.getElementById('panel-grid').classList.toggle('visible', type === 'grid');
    document.getElementById('panel-list').classList.toggle('visible', type === 'list');

    // Buttons
    document.getElementById('btn-grid').classList.toggle('active', type === 'grid');
    document.getElementById('btn-list').classList.toggle('active', type === 'list');
}




// For audio sound
const links = document.querySelectorAll('button');
const sound = document.getElementById('click-sound');

links.forEach(link => {
    link.addEventListener('click', function () {
        sound.currentTime = 0;
        sound.play();
        console.log(sound)
    });
});



// for submit form
const successSound = document.getElementById('success-sound');
const errorSound = document.getElementById('error-sound');

const submitBtns = document.querySelectorAll('form button');

submitBtns.forEach(btn => {
    btn.addEventListener('click', function (e) {

        const form = this.closest('form');

        if (form.checkValidity()) {
            successSound.currentTime = 0;
            successSound.play();
            console.log("Success");

        } else {
            errorSound.currentTime = 0;
            errorSound.play();
            console.log("Error");

            form.reportValidity();
        }
    });
});








// ==========  For  Search  ===========
function searchF(cardSelector, nameSelector, idSelector) {

    const searchInput = document.querySelector('.search-input')
    const cards = document.querySelectorAll(cardSelector)
    const errorContainer = document.getElementById('error-container')

    if (cards.length == 0) {
        errorContainer.classList.remove('d-none')
    }

    // validation 
    if (!searchInput || !cards.length || !errorContainer) {
        console.log('Required Elements not found')
        console.log('searchInput', searchInput, 'cards', cards, 'errorContainer', errorContainer)
        return
    }

    // search event
    searchInput.addEventListener('keyup', function () {
        const value = this.value.trim().toLowerCase()
        let found = false

        // if value empty then all card show
        if (value === '') {
            cards.forEach(card => card.style.display = 'block')
            errorContainer.classList.add('d-none')
            return
        }

        cards.forEach(card => {
            const nameEl = card.querySelector(nameSelector)
            const idEl = card.querySelector(idSelector)

            if (!nameEl || !idEl) return

            const cardName = nameEl.innerText.toLowerCase()
            const cardId = idEl.getAttribute('href').split('/').pop()

            if (cardName.includes(value) || cardId.includes(value)) {
                card.style.display = 'block'
                found = true;
            }
            else {
                card.style.display = 'none'
            }
        })

        if (found) {
            errorContainer.classList.add('d-none')    // hide
        } else {
            errorContainer.classList.remove('d-none') // show
        }
    })
}
