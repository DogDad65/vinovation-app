function showTab(event, tabId) {
    const tabs = event.target.parentNode.children;
    const contents = event.target.parentNode.nextElementSibling.children;

    // Remove 'active' class from all tabs and hide all tab contents
    for (let tab of tabs) tab.classList.remove("active");
    for (let content of contents) content.classList.add("hidden");

    // Add 'active' class to clicked tab and show the selected content
    event.target.classList.add("active");
    document.getElementById(tabId).classList.remove("hidden");
}

console.log("Dashboard JavaScript loaded successfully.");
