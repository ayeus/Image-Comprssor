document.getElementById('fileUpload').addEventListener('change', (event) => {
    const file = event.target.files[0];
    const fileSize = (file.size / 1024).toFixed(2); // Convert to KB
    document.getElementById('fileSize').innerText = `File Size: ${fileSize} KB`;
});

document.getElementById('compressBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileUpload');
    const desiredSizeInput = document.getElementById('desiredSize');
    const resultDiv = document.getElementById('result');

    if (!fileInput.files[0]) {
        alert('Please select a file to compress.');
        return;
    }

    const file = fileInput.files[0];
    const desiredSizeKB = desiredSizeInput.value;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('desired_size_kb', desiredSizeKB);

    try {
        const response = await fetch('http://127.0.0.1:5000/compress', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Compression failed');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Display the download link
        resultDiv.innerHTML = `
            <p>File compressed successfully!</p>
            <a href="${url}" download="compressed_${file.name}">Download Compressed File</a>
        `;
    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});