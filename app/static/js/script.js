// Quand on clique sur une tâche -> barrer/débarrer
document.addEventListener("DOMContentLoaded", () => {
    const taskItems = document.querySelectorAll(".task-item");

    taskItems.forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("completed");
        });
    });
});
