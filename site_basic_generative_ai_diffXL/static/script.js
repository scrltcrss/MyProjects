// Theme switcher functionality
const themeSwitch = document.getElementById('theme-switch');
themeSwitch.addEventListener('change', () => {
    // Toggle dark theme class on body
    document.body.classList.toggle('dark-theme');
    // Save theme preference to localStorage
    localStorage.setItem('darkThemeEnabled', themeSwitch.checked);
});

// Event listener for generate button
document.querySelector('.generate-btn').addEventListener('click', function() {
    // Display loader when generating image
    const loader = document.getElementById('global-loader');
    loader.style.display = 'block';
    // Hide previously generated image if any
    const image = document.getElementById('generated-image');
    if (image) {
        image.style.display = 'none';
    }
});

// Event listener for page load
window.addEventListener('load', () => {
    // Check for saved dark theme preference in localStorage
    const darkThemeEnabled = localStorage.getItem('darkThemeEnabled');
    // Apply dark theme if preference is true
    if (darkThemeEnabled && darkThemeEnabled === 'true') {
        document.body.classList.add('dark-theme');
        themeSwitch.checked = true;
    }
});

// Function to hide loader and display generated image
function hideLoader() {
    const loader = document.getElementById('global-loader');
    loader.style.display = 'none';
    const image = document.getElementById('generated-image');
    if (image) {
        image.style.display = 'block';
    }
}
