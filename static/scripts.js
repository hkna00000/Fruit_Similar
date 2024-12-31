document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const chosenImage = document.getElementById('chosenImage');
    chosenImage.style.display = 'block';
    chosenImage.src = URL.createObjectURL(fileInput.files[0]);
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });
    
    const result = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    if (result.error) {
        resultsDiv.textContent = `Error: ${result.error}`;
    } else {
        result.similar_images.forEach((imageName) => {
            const imageFrame = document.createElement('div');
            imageFrame.classList.add('image-frame');
            
            const imgElement = document.createElement('img');
            imgElement.src = imageName;
            imgElement.alt = imageName;
            imgElement.classList.add('result-image');
            
            imageFrame.appendChild(imgElement);
            resultsDiv.appendChild(imageFrame);
        });
    }
});