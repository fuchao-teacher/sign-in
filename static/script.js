function submitAnswer() {
    const name = document.getElementById('name').value;
    const selectedOption = document.querySelector('input[name="answer"]:checked');

    if (!selectedOption) {
        alert("请先选择一个答案！");
        return;
    }

    const answer = selectedOption.value;

    if (!name) {
        alert("请填写你的名字！");
        return;
    }

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, answer: answer }),
    })
    .then(response => response.json())
    .then(data => {
        const feedback = document.getElementById('feedback');
        if (data.status === 'success') {
            feedback.innerText = data.message;
            feedback.style.color = 'green';
        } else {
            feedback.innerText = data.message;
            feedback.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
