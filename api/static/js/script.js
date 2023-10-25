document.getElementById("save-button").addEventListener("click", () => {

    const userInput = collectUserInput();

    const inputDatFile = createdatFile(userInput);

    fetchSolutionFile(inputdatFile);

});

function collectUserInput() {

}

