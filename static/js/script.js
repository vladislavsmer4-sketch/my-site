const languageButton = document.querySelector(".language-button");
const languageSwitcher = document.querySelector(".language-switcher");

if (languageButton && languageSwitcher) {
    languageButton.addEventListener("click", function () {
        languageSwitcher.classList.toggle("open");
    });
}