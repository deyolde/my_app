document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('fileInput');
    const submitButton = document.getElementById('submitButton');
    const fileLabel = document.getElementById('fileLabel');
    const conversionTypeInput = document.getElementById('conversionTypeInput');
    const tabButtons = document.querySelectorAll('.tab-button');
  
    // Manejo de solapas: actualiza el tipo de conversión y la configuración del input
    tabButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Quita la clase activa de todas las solapas y la asigna a la seleccionada
        tabButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
  
        // Actualiza el campo oculto con el tipo de conversión
        const conversionType = this.getAttribute('data-conversion');
        conversionTypeInput.value = conversionType;
  
        // Modifica el atributo "accept" y el texto del label según la opción elegida
        if (conversionType === 'text_to_audio') {
          fileInput.accept = '.txt';
          fileLabel.textContent = 'Sube tu archivo TXT';
        } else if (conversionType === 'audio_to_text') {
          fileInput.accept = '.wav, .mp3, .ogg, .m4a';
          fileLabel.textContent = 'Sube tu archivo de audio';
        } else if (conversionType === 'video_to_audio') {
          fileInput.accept = 'video/*';
          fileLabel.textContent = 'Sube tu archivo de video';
        }
        // Reinicia el input y deshabilita el botón de envío
        fileInput.value = "";
        submitButton.disabled = true;
        submitButton.classList.remove('enabled');
      });
    });
  
    // Habilita el botón de envío cuando se selecciona un archivo
    fileInput.addEventListener('change', function() {
      if (fileInput.files.length > 0) {
        submitButton.disabled = false;
        submitButton.classList.add('enabled');
      } else {
        submitButton.disabled = true;
        submitButton.classList.remove('enabled');
      }
    });
  });
  