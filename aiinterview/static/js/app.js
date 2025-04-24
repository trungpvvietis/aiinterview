// public/static/js/interview.js

$(document).ready(function () {
    console.log("Interview page loaded!");

    // Example: WebSocket connection
    const sessionId = $("#session-id").data("session-id");
    const socket = new WebSocket(`ws://${window.location.host}/ws/interview/${sessionId}/`);
    
    $("#btn-start").click(function() {
        console.log("Start Interview")
        socket.send(JSON.stringify({ type: "start_interview" }));
    })
    $("#btn-cancel").click(function() {
        console.log("Cancel Interview")
        socket.send(JSON.stringify({ type: "cancel_interview" }));
    })
    // navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
    //     const mediaRecorder = new MediaRecorder(stream, {
    //         mimeType: 'video/webm; codecs=vp8,opus'
    //     });
    
    //     mediaRecorder.start(3000);  // send every 3 seconds
    
    //     mediaRecorder.ondataavailable = function (event) {
    //         if (event.data.size > 0) {
    //             event.data.arrayBuffer().then(buffer => {
    //                 socket.send(buffer); // send raw binary
    //             });
    //         }
    //     };
    // });
    
    // When message received from Django Channels
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("Received data:", data);

        if (data.type === "connect") {
            if (data.message.status != "scheduled" && data.message.status != "in_progress") {
                $("#note-id").text(`Buổi phỏng vấn đã ${data.message.status}`)
            } else if (data.message.unanswered_question) {
                liveStream()
                $("#note-id").text(`Bạn chưa trả lời câu hỏi số ${data.message.unanswered_question.question_id}`)
            } else if (data.message.next_interview_question) {
                liveStream()
                $("#note-id").text(`Hãy trả lời câu hỏi dưới đây`)
                typeText("#question-box", data.message.next_interview_question.question_text);
            }
        }

        if (data.type === "questions") {
            typeText("#question-box", data.data.question);
        }
        if (data.type == "start_interview") {
            if (data.message.status != "scheduled" && data.message.status != "in_progress") {
                $("#note-id").text(`Buổi phỏng vấn đã ${data.message.status}`)
            } else if (data.message.unanswered_question) {
                $("#note-id").text(`Bạn chưa trả lời câu hỏi số ${data.message.unanswered_question.question_id}`)
            } else if (data.message.next_interview_question) {
                $("#note-id").text(`Hãy trả lời câu hỏi dưới đây`)
            }
        }
        if (data.type == "cancel_interview") {
            $("#note-id").text(data.message)
        }
    };

    socket.onopen = function () {
        console.log("WebSocket connected.");
    };

    socket.onclose = function () {
        console.log("WebSocket disconnected.");
    };

    function liveStream() {
        const videoPreview = document.getElementById("preview");
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then((stream) => {
            videoPreview.srcObject = stream;
            videoPreview.play();

            mediaRecorder = new MediaRecorder(stream, {
                mimeType: "video/webm; codecs=vp8,opus"
            });
    
            mediaRecorder.ondataavailable = function (event) {
                if (event.data && event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
                    event.data.arrayBuffer().then(buffer => {
                        socket.send(buffer);
                    });
                }
            };
    
            mediaRecorder.start(2000); // every 2 seconds
        })
        .catch((err) => {
          console.error("Error accessing camera/microphone:", err);
        });
    }

    // Render interview questions
    function typeText(selector, text, speed = 40) {
        const el = $(selector);
        el.empty();
    
        let i = 0;
        function typeChar() {
            if (i < text.length) {
                el.append(text.charAt(i));
                i++;
                setTimeout(typeChar, speed);
            }
        }
        typeChar();
    }
});
