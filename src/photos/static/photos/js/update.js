const tagsDataElement = document.getElementById('tags-data');
const selectedTagsDataElement = document.getElementById('selected-tags-data');

let availableTags = [];
let tags = [];

if (tagsDataElement) {
    availableTags = JSON.parse(tagsDataElement.textContent);
}

if (selectedTagsDataElement) {
    const initialTags = JSON.parse(
        selectedTagsDataElement.textContent
    );

    if (Array.isArray(initialTags)) {
        tags = initialTags.map(
            tag => tag.trim().toLowerCase()
        );
    }
}

const caption = document.getElementById('caption');
const captionCount = document.getElementById('caption-count');

const tagInput = document.getElementById('tag-input');
const selectedTags = document.getElementById('selected-tags');
const suggestions = document.getElementById('tag-suggestions');
const hiddenInput = document.getElementById('id_tags');


function updateCaptionCount() {
    if (!caption || !captionCount) return;

    const length = caption.value.length;

    captionCount.textContent = `${length} / 200`;

    if (length > 180) {
        captionCount.style.color = '#e74c3c';
    } else if (length > 150) {
        captionCount.style.color = '#f39c12';
    } else {
        captionCount.style.color = '';
    }
}

caption?.addEventListener('input', updateCaptionCount);

updateCaptionCount();


function isValidTag(tag) {
    return availableTags.some(
        availableTag =>
            availableTag.toLowerCase() === tag.toLowerCase()
    );
}


function renderTags() {
    selectedTags.innerHTML = '';

    tags.forEach(tag => {
        const chip = document.createElement('span');
        chip.className = 'tag-chip';

        const text = document.createElement('span');
        text.textContent = tag;

        const button = document.createElement('button');

        button.type = 'button';
        button.textContent = '×';
        button.setAttribute(
            'aria-label',
            `Remove ${tag}`
        );

        button.addEventListener('click', () => {
            tags = tags.filter(
                item => item !== tag
            );

            renderTags();
        });

        chip.appendChild(text);
        chip.appendChild(button);

        selectedTags.appendChild(chip);
    });

    hiddenInput.value = tags.join(',');
}


function addTag(value) {
    const tag = value.trim().toLowerCase();

    if (!tag) return;

    if (!isValidTag(tag)) {
        alert(`Tag "${tag}" is not available.`);
        return;
    }

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
        .filter(tag =>
            tag.toLowerCase().includes(query)
        )
        .filter(tag =>
            !tags.includes(tag.toLowerCase())
        )
        .slice(0, 5);

    filtered.forEach(tag => {
        const button = document.createElement('button');

        button.type = 'button';
        button.textContent = tag;
        button.className = 'suggestion-item';

        button.addEventListener('click', () => {
            addTag(tag);
        });

        suggestions.appendChild(button);
    });
});


tagInput?.addEventListener('keydown', event => {
    if (event.key !== 'Enter') return;

    event.preventDefault();

    addTag(tagInput.value);
});


document.addEventListener('click', event => {
    if (
        !event.target.closest('.tags-input') &&
        !event.target.closest('.tag-suggestions')
    ) {
        suggestions.innerHTML = '';
    }
});


renderTags();
