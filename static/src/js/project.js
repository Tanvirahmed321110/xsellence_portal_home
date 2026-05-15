document.addEventListener("DOMContentLoaded", function () {

    (function () {
        const urlParams = new URLSearchParams(window.location.search);
        const status = urlParams.get('status');
        if (status) {
            const select = document.getElementById('filter-status');
            select.value = status;
        }
    })();


    // const searchInput = document.querySelector('.search-input');
    // const projectCards = document.querySelectorAll('.proj-card');
    // const errorContainer = document.querySelector('#error-container');

    // // searchInput.addEventListener('keyup', function () {
    // //     const value = this.value.toLowerCase()
    // //     let found = false

    // //     projectCards.forEach(card => {
    // //         const projectName = card
    // //     })
    // // })


    // searchInput.addEventListener('keyup', function () {

    //     const value = this.value.toLowerCase();

    //     projectCards.forEach(card => {

    //         const projectName = card
    //             .querySelector('.card-proj-name')
    //             .innerText
    //             .toLowerCase();

    //         const projectLink = card
    //             .querySelector('.btn-primary')
    //             .getAttribute('href');

    //         const projectId = projectLink.split('/').pop();

    //         if (
    //             projectName.includes(value) ||
    //             projectId.includes(value)
    //         ) {
    //             card.style.display = 'block';
    //         } else {
    //             card.style.display = 'none';
    //         }

    //     });

    // });


    function initProjectSearch() {

        const searchInput = document.querySelector('.search-input');
        const projectCards = document.querySelectorAll('.proj-card');
        const errorContainer = document.querySelector('#error-container');

        // Validation
        if (!searchInput || !projectCards.length || !errorContainer) {
            console.error('Required elements found না।');
            return;
        }

        searchInput.addEventListener('keyup', function () {

            const value = this.value.trim().toLowerCase();
            let found = false;

            // খালি হলে সব দেখাও
            if (value === '') {
                projectCards.forEach(card => card.style.display = 'block');
                errorContainer.classList.add('d-none');
                return;
            }

            projectCards.forEach(card => {

                const nameEl = card.querySelector('.card-proj-name');
                const linkEl = card.querySelector('.btn-primary.action-btn');

                if (!nameEl || !linkEl) return; // card broken হলে skip

                const projectName = nameEl.innerText.toLowerCase();
                const projectId = linkEl.getAttribute('href').split('/').pop();

                if (projectName.includes(value) || projectId.includes(value)) {
                    card.style.display = 'block';
                    found = true;
                } else {
                    card.style.display = 'none';
                }
            });

            errorContainer.classList.toggle('d-none', found);
        });
    }

    initProjectSearch()


});