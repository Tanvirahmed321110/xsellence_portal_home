
//============== for Notification
const notificationSidebar = document.getElementById('notification-sidebar');

if (notificationSidebar) {

    const overlay = document.getElementById('overlay');

    // open button
    document.getElementById('notification-btn').onclick = () => {
        notificationSidebar.classList.add('open');
        overlay.classList.add('show');
        console.log('click')
    }

    // close button
    document.getElementById('close3').onclick = close;
    overlay.onclick = close;

    function close() {
        notificationSidebar.classList.remove('open');
        overlay.classList.remove('show');
    }
}
else {
    console.log('notificationSidebar not found')
}

//============== For Delete Confirmation
function openDeleteModal(element) {
    let modal = document.getElementById('deleteModal');
    let confirmBtn = document.getElementById('confirmYes');
    if (!modal || !confirmBtn) return false;

    // ✅ href এর বদলে form submit
    let form = element.closest('form');
    confirmBtn.onclick = function () {
        form.submit();
    };

    modal.classList.add('active');
    return false;
}

function closeModal(modalId) {
    let modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('active');
}

function deleteModalF(deleteModal) {
    let modal = document.getElementById('deleteModal');
    if (!modal) return;
    modal.addEventListener('click', function (e) {
        if (e.target === this) closeModal(deleteModal);
    });
}



//==============  For List and Grid View  (Global)
function setView(type) {
    document.getElementById('panel-grid').classList.toggle('visible', type === 'grid');
    document.getElementById('panel-list').classList.toggle('visible', type === 'list');
    document.getElementById('btn-grid').classList.toggle('active', type === 'grid');
    document.getElementById('btn-list').classList.toggle('active', type === 'list');
}


// ============  For Search  (Global)
function searchF(cardSelector, nameSelector, idSelector) {

    const searchInput = document.querySelector('.search-input')
    const cards = document.querySelectorAll(cardSelector)
    const listRows = document.querySelectorAll('#panel-list tbody tr')

    // ✅ Get or CREATE error container dynamically
    let errorContainer = document.getElementById('error-container')

    if (!errorContainer) {
        errorContainer = document.createElement('div')
        errorContainer.id = 'error-container'
        errorContainer.innerHTML = `
            <div class="design-wrapper mt-7">
                <div class="empty-4">
                    <div class="e4-glass">
                        <div class="e4-ring">
                            <span class="e4-icon-center">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                    <circle cx="11" cy="11" r="7"></circle>
                                    <path d="M16.5 16.5L21 21"></path>
                                    <line x1="8" y1="11" x2="14" y2="11"></line>
                                </svg>
                            </span>
                        </div>
                        <h2 class="e4-title">Data <strong style="color: red;">'NOT'</strong> Found</h2>
                        <p class="e4-sub">No records matched your current search or filter criteria.</p>
                        <div class="e4-pills">
                            <span class="e4-pill">0 results</span>
                            <span class="e4-pill">try new filter</span>
                            <span class="e4-pill">clear search</span>
                        </div>
                    </div>
                </div>
            </div>
        `
        errorContainer.style.display = 'none' // hidden by default

        // ✅ Insert after the cards container
        const panel = document.getElementById('panel-grid')
        panel.parentNode.insertBefore(errorContainer, panel.nextSibling)
    }

    // validation
    if (!searchInput || !cards.length) {
        console.log('Required Elements not found')
        return
    }

    // search event
    searchInput.addEventListener('keyup', function () {
        const value = this.value.trim().toLowerCase()
        let found = false

        if (value === '') {
            cards.forEach(card => card.style.display = 'block')
            listRows.forEach(row => row.style.display = '')
            errorContainer.style.display = 'none'
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
                found = true
            } else {
                card.style.display = 'none'
            }
        })

        listRows.forEach(row => {
            const name = row.children[0].innerText.toLowerCase()
            const idEl = row.querySelector('.btn-primary')

            let rowId = ''
            if (idEl) {
                rowId = idEl.getAttribute('href').split('/').pop()
            }

            if (name.includes(value) || rowId.includes(value)) {
                row.style.display = ''
                found = true
            } else {
                row.style.display = 'none'
            }
        })

        // ✅ show/hide with style.display instead of classList
        errorContainer.style.display = found ? 'none' : 'block'
    })
}




document.addEventListener("DOMContentLoaded", function () {

    //=============  Sidebar
    const sidebar = document.getElementById('sidebar');

    function openSidebarDesktop() {
    const collaps_btn = document.getElementById('collaps-btn');
    const main_content = document.querySelector('.main-content');
    const notic_board = document.getElementById('notic-board');

    if (!collaps_btn || !main_content || !sidebar || !notic_board) {
        console.log("Sidebar elements not found ❌");
        return;
    }

    // Page load হলে previous state apply
    const isCollapsed = localStorage.getItem('sidebarCollapsed');

    if (isCollapsed === 'true') {
        sidebar.classList.add('sidebar-small');
        main_content.classList.add('main-content-big');
        notic_board.classList.add('big');
    }

    collaps_btn.addEventListener('click', function () {
        sidebar.classList.toggle('sidebar-small');
        main_content.classList.toggle('main-content-big');
        notic_board.classList.toggle('big');

        // Save state
        localStorage.setItem(
            'sidebarCollapsed',
            sidebar.classList.contains('sidebar-small')
        );
    });
}

openSidebarDesktop();




    //===============  For Mobile Sidebar
    function mobileSidebar() {
        const mobile_menu_btn = document.getElementById('mobile-menu-btn')
        const menuIcon = document.getElementById('menu-icon');

        if (!mobile_menu_btn || !menuIcon) {
            console.log("Sidebar elements not found ❌");
            return;
        }

        let isOpen = false;

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




    //============= For Theme Button
    // const toggle = document.getElementById("themeToggle");
    //
    // toggle.addEventListener("click", () => {
    //     const currentTheme = document.documentElement.getAttribute("data-theme");
    //
    //     if (currentTheme === "dark") {
    //         document.documentElement.setAttribute("data-theme", "light");
    //         localStorage.setItem("theme", "light");
    //     } else {
    //         document.documentElement.setAttribute("data-theme", "dark");
    //         localStorage.setItem("theme", "dark");
    //     }
    // });




    // ============  For Date input field Change Placeholder color
    document.querySelectorAll('input[type="date"]').forEach(function (input) {
        toggleDateColor(input);

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




    // for current date
//    const dateEl = document.querySelector('header .date span')
//    const today = new Date()
//    const options = { day: "2-digit", month: "short", year: 'numeric' }
//    dateEl.innerText = today.toLocaleDateString('en-GB', options)


// date and time show update
    const dateEl = document.getElementById('live-date');
    const timeEl = document.getElementById('live-time');
    if (!dateEl || !timeEl) return;

    function updateDateTime() {
    const now = new Date();
    dateEl.textContent = now.toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric',
        timeZone: 'Asia/Dhaka'
    });
    timeEl.textContent = now.toLocaleTimeString('en-GB', {
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false,
        timeZone: 'Asia/Dhaka'
    });
}

    updateDateTime();
    setInterval(updateDateTime, 1000);


    // For audio sound
    const links = document.querySelectorAll('button');
    const sound = document.getElementById('click-sound');

    links.forEach(link => {
        link.addEventListener('click', function () {
            sound.currentTime = 0;
            sound.play();
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




    //  ===============  For Status Filter
    function setStatusFilter() {
        const select = document.getElementById('filter-status')
        if (!select) return
        const status = new URLSearchParams(window.location.search).get('status')
        if (status && select) select.value = status
    }
    setStatusFilter()



    //============   For Dropdown Open  ===========
    document.addEventListener("click", function (event) {
        const label = event.target.closest(".select-open-label");
        if (!label) return;

        const selectId = label.dataset.selectTarget;
        const select = document.getElementById(selectId);
        if (!select) return;

        select.focus();

        if (typeof select.showPicker === "function") {
            select.showPicker();
        } else {
            select.click();
        }
    });



});



// Dashboard dark theme toggle
(function () {
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('dashboardTheme');

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }

    window.toggleTheme = function () {
        document.body.classList.toggle('dark-theme');

        const activeTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('dashboardTheme', activeTheme);
    };

    if (themeToggle) {
        themeToggle.setAttribute('title', 'Theme');
        themeToggle.setAttribute('aria-label', 'Toggle dark theme');
        themeToggle.addEventListener('click', window.toggleTheme);
    }
})();
