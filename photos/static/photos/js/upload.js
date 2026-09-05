const tagsDataElement = document.getElementById('tags-data');
let availableTags = [];

if (tagsDataElement) {
    try {
        availableTags = JSON.parse(tagsDataElement.textContent);
    } catch (e) {
        availableTags = [];
    }
}

const photoInput = document.getElementById('id_image');
const fileName = document.getElementById('file-name');
const fileField = document.querySelector('.file-field');

photoInput?.addEventListener('change', function () {
    const file = this.files[0];
    if (!file || !file.type.startsWith('image/')) {
        this.value = '';
        fileName.textContent = 'Choose a photo...';
        fileField.classList.remove('has-file');
        return;
    }
    fileName.textContent = file.name;
    fileField.classList.add('has-file');
});

const caption = document.getElementById('id_caption');
const captionCount = document.getElementById('caption-count');

caption?.addEventListener('input', () => {
    const length = caption.value.length;
    captionCount.textContent = `${length} / 200`;
    if (length > 180) {
        captionCount.style.color = '#e74c3c';
    } else if (length > 150) {
        captionCount.style.color = '#f39c12';
    } else {
        captionCount.style.color = '';
    }
});

const tagInput = document.getElementById('tag-input');
const selectedTags = document.getElementById('selected-tags');
const suggestions = document.getElementById('tag-suggestions');
const hiddenInput = document.getElementById('id_tags');

let tags = [];

function renderTags() {
    selectedTags.innerHTML = '';
    const tagString = tags.join(',');

    tags.forEach((tag) => {
        const chip = document.createElement('span');
        chip.className = 'tag-chip';
        chip.innerHTML = `<span>${tag}</span><button type="button" aria-label="Remove ${tag}">×</button>`;

        chip.querySelector('button').addEventListener('click', () => {
            tags = tags.filter((item) => item !== tag);
            renderTags();
        });

        selectedTags.appendChild(chip);
    });

    if (hiddenInput) {
        hiddenInput.value = tagString;
    }
}

function addTag(value) {
    const tag = value.trim().toLowerCase();
    if (!tag) return;
    if (tags.includes(tag)) {
        alert('This tag is already added.');
        return;
    }
    if (tags.length >= 8) {
        alert('Maximum 8 tags allowed.');
        return;
    }
    tags.push(tag);
    tagInput.value = '';
    suggestions.innerHTML = '';
    renderTags();
}

tagInput?.addEventListener('input', () => {
    const query = tagInput.value.trim().toLowerCase();
    suggestions.innerHTML = '';
    if (!query) return;

    const filtered = availableTags
        .filter((tag) => tag.toLowerCase().includes(query))
        .filter((tag) => !tags.includes(tag.toLowerCase()))
        .slice(0, 5);

    filtered.forEach((tag) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = tag;
        button.className = 'suggestion-item';
        button.addEventListener('click', () => addTag(tag));
        suggestions.appendChild(button);
    });
});

tagInput?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        const query = tagInput.value.trim().toLowerCase();
        if (query) {
            addTag(query);
        }
    }
});

document.addEventListener('click', (event) => {
    if (!event.target.closest('.tags-input') && !event.target.closest('.tag-suggestions')) {
        suggestions.innerHTML = '';
    }
});

renderTags();
