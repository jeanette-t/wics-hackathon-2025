function generateStory() {
    // Retrieve stored user inputs
    const favoriteColor = localStorage.getItem("favoriteColor") || "blue";
    const favoriteAnimal = localStorage.getItem("favoriteAnimal") || "dog";
    const favoriteHobby = localStorage.getItem("favoriteHobby") || "reading";
    const userName = localStorage.getItem("userName") || "Alex";

    // Construct the story
    const story = `
        Once upon a time, there was a person named ${userName} who loved the color ${favoriteColor}.
        One day, ${userName} met a magical ${favoriteAnimal} that could talk! The two became best friends
        and spent their days ${favoriteHobby} together. It was the beginning of a wonderful adventure!
    `;

    // Display the story in the paragraph element
    document.getElementById("story-text").innerText = story;
}

// Call function to generate story on page load
window.onload = generateStory;