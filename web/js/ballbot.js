document.getElementById("motor-form").addEventListener("click", function(event) {
    if (event.target.tagName === "BUTTON") {
        event.preventDefault();
        const cmd = event.target.value;

        fetch("/control", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `cmd=${cmd}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("서버 오류");
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("status").textContent = `모터 명령 전송됨: ${cmd}`;
        })
        .catch(error => {
            document.getElementById("status").textContent = "서버 응답 오류!";
        });
    }
});