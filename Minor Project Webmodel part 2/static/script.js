console.log('Script loaded');
function displayFileName() {
    const fileInput = document.getElementById('fileinput');
    const fileNameSpan = document.getElementById('fileName');

    if (fileInput.files.length > 0) {
        fileNameSpan.textContent = fileInput.files[0].name;
    } else {
        fileNameSpan.textContent = 'No file chosen';
    }
}

// Ensure the script is placed at the end of the HTML body or use the defer attribute in the script tag.
