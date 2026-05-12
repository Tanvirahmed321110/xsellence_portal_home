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


const searchInput = document.querySelector('.search-input');
const projectCards = document.querySelectorAll('.proj-card');
const errorContainer = document.querySelector('#error-container');



searchInput.addEventListener('keyup', function () {

    const value = this.value.toLowerCase();
    let found = false;

    projectCards.forEach(card => {

        const projectName = card.querySelector('.card-proj-name').innerText.toLowerCase();
        const projectLink = card.querySelector('.btn-primary.action-btn').getAttribute('href');
        const projectId = projectLink.split('/').pop();

        if (projectName.includes(value) || projectId.includes(value)) {
            card.style.display = 'block';
            found = true;
        }
        else {
            card.style.display = 'none';
        }

    });

    // ===== Show / Hide Error Container =====
    if (found) {
        errorContainer.classList.add('d-none');
    } else {
        errorContainer.classList.remove('d-none');
    }

});