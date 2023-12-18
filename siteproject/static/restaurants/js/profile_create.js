function setupImagePreview(input, previewId) {
    const previewImage = document.getElementById(previewId);

    input.addEventListener('change', function() {
      if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
          previewImage.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
      }
    });
  }

  setupImagePreview(document.querySelector('input[name="restaurant_image"]'), 'preview-image-main');
  setupImagePreview(document.querySelector('input[name="photo_1"]'), 'preview-image-1');
  setupImagePreview(document.querySelector('input[name="photo_2"]'), 'preview-image-2');
  setupImagePreview(document.querySelector('input[name="photo_3"]'), 'preview-image-3');