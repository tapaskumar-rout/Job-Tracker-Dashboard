document.addEventListener("DOMContentLoaded", () => {
  const editor = document.getElementById("editor");

  if (!editor) return;

  const quill = new Quill("#editor", {
    theme: "snow",
    plceholder: "Write notes...",
    modules: {
      toolbar: [
        [{ header: [1,2,false]}],
        ["bold", "italic","underline"],
        [{ list: "ordered"}, { list: "bullet"}],
        ["link"],
        ["clean"]
      ]
    }
  });

  const hiddenInput = document.getElementById("notes");

  if (hiddenInput.value) {
    quill.root.innerHTML = hiddenInput.value;
  }

  editor.closest("form").onsubmit = function (){
    hiddenInput.value = quill.root.innerHTML;
  };
});