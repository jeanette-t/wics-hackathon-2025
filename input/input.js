document.getElementById("storyForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Stop form from refreshing the page

    // Get input values
    let userData = {
        name: document.getElementById("name").value,
        color: document.getElementById("color").value,
        animal: document.getElementById("animal").value,
        place: document.getElementById("place").value,
        food: document.getElementById("food").value
    };

    // Save to localStorage for later use
    localStorage.setItem("storyData", JSON.stringify(userData));

    // Redirect to the next page where the story is generated
    window.location.href = "story.html";
});