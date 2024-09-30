function toggleModifications(mainItem, modificationDivId) {
    var modificationDiv = document.getElementById(modificationDivId);
    if (mainItem.checked) {
        modificationDiv.style.display = 'block';
    } else {
        modificationDiv.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var modifications = document.getElementById('modification');
    modifications.style.display = 'none'; 
});