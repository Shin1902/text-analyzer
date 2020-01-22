window.onload = () => {

  const fileInput = document.getElementById('uploading_file');
  
  fileInput.addEventListener("change", (e) => {
    console.log("works");
    for (let i = 0, len = fileInput.files.length; i < len; i++) {
      console.log(fileInput.files[i].name);
      document.getElementById('selected_filename').innerHTML = fileInput.files[i].name;
    }
  });

}