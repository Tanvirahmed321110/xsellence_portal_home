document.addEventListener("DOMContentLoaded", function () {

    (function () {
        const urlParams = new URLSearchParams(window.location.search);
        const status = urlParams.get('status');
        if (status) {
            const select = document.getElementById('filter-status');
            select.value = status;
        }
    })();



    // function searchF(cardSelector) {

    //     const searchInput = document.querySelector('.search-input');
    //     const card = document.querySelectorAll(cardSelector);
    //     const errorContainer = document.querySelector('#error-container');

    //     // Validation
    //     if (!searchInput || !card.length || !errorContainer) {
    //         console.error('Required elements not found');
    //         return;
    //     }

    //     searchInput.addEventListener('keyup', function () {

    //         const value = this.value.trim().toLowerCase();
    //         let found = false;

    //         // খালি হলে সব দেখাও
    //         if (value === '') {
    //             card.forEach(card => card.style.display = 'block');
    //             errorContainer.classList.add('d-none');
    //             return;
    //         }

    //         card.forEach(card => {

    //             const nameEl = card.querySelector('.card-proj-name');
    //             const linkEl = card.querySelector('.btn-primary.action-btn');

    //             if (!nameEl || !linkEl) return; // card broken হলে skip

    //             const projectName = nameEl.innerText.toLowerCase();
    //             const projectId = linkEl.getAttribute('href').split('/').pop();

    //             if (projectName.includes(value) || projectId.includes(value)) {
    //                 card.style.display = 'block';
    //                 found = true;
    //             } else {
    //                 card.style.display = 'none';
    //             }
    //         });

    //         errorContainer.classList.toggle('d-none', found);
    //     });
    // }

    // searchF('.proj-card')



    // for project page
    searchF('.proj-card', '.card-proj-name', '.btn-primary.action-btn')



});