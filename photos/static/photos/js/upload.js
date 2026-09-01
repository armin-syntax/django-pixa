const photoInput = document.getElementById('photo');
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

const caption = document.getElementById('caption');
const captionCount = document.getElementById('caption-count');

caption?.addEventListener('input', () => {
  captionCount.textContent = `${caption.value.length} / 200`;
});

const tagInput = document.getElementById('tag-input');
const selectedTags = document.getElementById('selected-tags');
const suggestions = document.getElementById('tag-suggestions');
const hiddenInputs = document.getElementById('tag-hidden-inputs');

const availableTags = [
  'minimal', 'modern', 'architecture', 'interior', 'nature',
  'travel', 'wood', 'home', 'design', 'green', 'city',
  'photography', 'plants', 'light', 'portrait', 'street'
];

let tags = [];

function renderTags() {
  selectedTags.innerHTML = '';
  hiddenInputs.innerHTML = '';

  tags.forEach((tag) => {
    const chip = document.createElement('span');
    chip.className = 'tag-chip';
    chip.innerHTML = `<span>${tag}</span><button type="button" aria-label="Remove ${tag}">×</button>`;

    chip.querySelector('button').addEventListener('click', () => {
      tags = tags.filter((item) => item !== tag);
      renderTags();
    });

    selectedTags.appendChild(chip);

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'tags';
    input.value = tag;
    hiddenInputs.appendChild(input);
  });
}

function addTag(value) {
  const tag = value.trim().toLowerCase();
  if (!tag || tags.includes(tag) || tags.length >= 8) return;
  tags.push(tag);
  tagInput.value = '';
  suggestions.innerHTML = '';
  renderTags();
}

tagInput?.addEventListener('input', () => {
  const query = tagInput.value.trim().toLowerCase();
  suggestions.innerHTML = '';
  if (!query) return;

  availableTags
    .filter((tag) => tag.includes(query) && !tags.includes(tag))
    .slice(0, 5)
    .forEach((tag) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = tag;
      button.addEventListener('click', () => addTag(tag));
      suggestions.appendChild(button);
    });
});

tagInput?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ',') {
    event.preventDefault();
    addTag(tagInput.value);
  }
});