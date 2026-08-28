document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ПОШУК
    ===================================================== */

    const searchForm = document.querySelector(".site-search");
    const searchButton = document.querySelector(".search-submit");
    const searchInput = document.querySelector(".site-search input");

    if (searchForm && searchButton && searchInput) {

        let searchOpened = false;

        searchButton.addEventListener("click", function (event) {

            if (!searchOpened) {
                event.preventDefault();

                searchOpened = true;

                searchForm.classList.add("search-open");

                searchForm.style.width = "";

                setTimeout(function () {
                    searchInput.focus();
                }, 50);

                return;
            }

            if (searchInput.value.trim() === "") {
                event.preventDefault();
                searchInput.focus();
            }
        });


        searchInput.addEventListener("blur", function () {

            if (searchInput.value.trim() === "") {

                searchOpened = false;

                searchForm.classList.remove("search-open");

                searchInput.value = "";
            }
        });


        searchForm.addEventListener("submit", function (event) {

            if (searchInput.value.trim() === "") {

                event.preventDefault();

                searchOpened = true;

                searchForm.classList.add("search-open");

                searchInput.focus();
            }
        });
    }


    /* =====================================================
       МОВА
    ===================================================== */

    const languageButton =
        document.querySelector(".language-button");

    const languageSwitcher =
        document.querySelector(".language-switcher");

    if (languageButton && languageSwitcher) {

        languageButton.addEventListener("click", function (event) {

            event.stopPropagation();

            languageSwitcher.classList.toggle("open");
        });

        document.addEventListener("click", function () {

            languageSwitcher.classList.remove("open");
        });
    }

})