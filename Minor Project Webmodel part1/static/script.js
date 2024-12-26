document.addEventListener("DOMContentLoaded", function () {
    const translationForm = document.getElementById("translationForm");
    const outputDiv = document.getElementById("outputDiv");

    translationForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Get the input sentence
        const sentenceInput = document.getElementById("sentence");
        const sentence = sentenceInput.value;

        // Perform your translation or transformation here
        const transformedSentence = transformSentence(sentence);

        // Display the result
        outputDiv.textContent = transformedSentence;
    });

    // Replace this function with your actual translation logic
    function transformSentence(sentence) {
        // Example transformation: Reverse the sentence
        return sentence.split("").join("");
    }
});



