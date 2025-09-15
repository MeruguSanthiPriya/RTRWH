document.addEventListener('DOMContentLoaded', () => {
    const languageSelect = document.getElementById('languageSelect');

    async function fetchTranslations(lang) {
        try {
            const response = await fetch(`/static/locales/${lang}/translation.json`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Could not fetch translations:", error);
            return {}; // Return empty object on error
        }
    }

    async function changeLanguage(lang) {
        const translations = await fetchTranslations(lang);
        
        document.querySelectorAll('[data-translate-key]').forEach(element => {
            const key = element.getAttribute('data-translate-key');
            if (translations[key]) {
                // Use innerHTML for elements that may contain HTML tags like <br>
                element.innerHTML = translations[key];
            }
        });

        localStorage.setItem('language', lang);
        if (languageSelect) {
            languageSelect.value = lang;
        }
    }

    if (languageSelect) {
        languageSelect.addEventListener('change', (event) => {
            changeLanguage(event.target.value);
        });
    }

    // On page load, set the language
    const savedLanguage = localStorage.getItem('language') || 'en';
    changeLanguage(savedLanguage);
});
