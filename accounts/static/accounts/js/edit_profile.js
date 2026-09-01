const profileImage = document.getElementById('profile-image');
const profilePreview = document.getElementById('profile-preview');

profileImage?.addEventListener('change', function () {
  const file = this.files[0];
  if (!file || !file.type.startsWith('image/')) {
    this.value = '';
    return;
  }
  profilePreview.src = URL.createObjectURL(file);
});

const bio = document.getElementById('bio');
const bioCount = document.getElementById('bio-count');

function updateBioCount() {
  if (bio && bioCount) {
    bioCount.textContent = `${bio.value.length} / 500`;
  }
}

bio?.addEventListener('input', updateBioCount);
updateBioCount();