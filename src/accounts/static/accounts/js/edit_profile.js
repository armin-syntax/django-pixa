const profileImage = document.getElementById('id_avatar');
const profilePreview = document.getElementById('profile-preview');

profileImage?.addEventListener('change', function () {
  const file = this.files[0];
  if (!file || !file.type.startsWith('image/')) {
    this.value = '';
    return;
  }

  if (profilePreview.tagName === 'DIV') {
    const img = document.createElement('img');
    img.id = 'profile-preview';
    img.alt = 'Profile picture';
    img.src = URL.createObjectURL(file);
    profilePreview.parentNode.replaceChild(img, profilePreview);
  } else {
    profilePreview.src = URL.createObjectURL(file);
  }
});

const bio = document.getElementById('id_bio');
const bioCount = document.getElementById('bio-count');

function updateBioCount() {
  if (bio && bioCount) {
    bioCount.textContent = `${bio.value.length} / 500`;
  }
}

bio?.addEventListener('input', updateBioCount);
updateBioCount();
