  document.addEventListener("DOMContentLoaded", function () {

                   console.log('modal:', document.getElementById('deleteModal'));
                    console.log('confirmYes:', document.getElementById('confirmYes'));
                    console.log('openDeleteModal:', typeof openDeleteModal);
                    deleteModalF('deleteModal');
                    searchF('.proj-card', '.card-proj-name', '.view-btn');
                });
