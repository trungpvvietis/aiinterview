// public/static/js/interview.js

$(document).ready(function () {
    console.log("Interview page loaded!");

    // Example: WebSocket connection
    const sessionId = $("#session-id").data("session-id");
    const socket = new WebSocket(`ws://${window.location.host}/ws/interview/${sessionId}/`);
    
    $("#btn-start").click(function() {
        console.log("Start Interview")
        socket.send(JSON.stringify({ type: "start_interview" }));
        liveStream()
        $(this).prop('disabled', true);
    })
    $("#btn-cancel").click(function() {
        console.log("Cancel Interview")
        socket.send(JSON.stringify({ type: "cancel_interview" }));
        $(this).prop('disabled', true);
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
        if (data.type == "is_answer_done") {
            console.log("is_answer_done", data)
            $("#note-id").text(`Cảm ơn câu trả lời của bạn! Hãy chuẩn bị trả lời cho cẩu hỏi tiếp theo...`)
        }
        if (data.type == "interview_completed") {
            console.log("interview_completed", data)
            $("#answer-box").text("");
            $("#question-box").text("");
            $("#note-id").text(`Buổi phỏng vấn đã kết thúc, xin cảm ơn bạn đã dành thời gian cho chúng tôi!`)

            $("#communication-id").text(data.message.communication_score);
            $("#challenge-id").text(data.message.challenge_score);
            $("#appearance-id").text(data.message.appearance_score);
            $("#facial-id").text(data.message.facial_score);
            $("#body_language-id").text(data.message.body_language_score);
            $("#environment-id").text(data.message.environment_score);
            $("#overall-id").text(data.message.overall_score);

        }
        if (data.type == "next_question") {
            $("#answer-box").text("");
            $("#note-id").text(`Hãy trả lời câu hỏi tiếp theo dưới đây!`)
            if (data.message.next_interview_question != undefined) {
                typeText("#question-box", data.message.next_interview_question.question_text);
            } else {
                typeText("#question-box", data.message.unanswered_question.question_text);
            }
        }

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
            } else if (data.message.status == "scheduled") {
                $("#note-id").text(`Click start để băt đầu buổi phỏng vấn`)
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
                typeText("#question-box", data.message.next_interview_question.question_text);
            }
        }
        if (data.type == "cancel_interview") {
            $("#note-id").text(data.message)
        }

        if (data.type == "chunk_answer_transcript") {
            console.log("CHUNK")
            typeText("#answer-box", data.message.answer_text);
        }
        if (data.type == "full_answer_transcript") {
            console.log("FULL")
            typeText("#answer-box", data.message.answer_text);
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
    function typeText(selector, text, speed = 20) {
        const el = $(selector);
        
        let i = 0;
    
        // Create cursor if not exists
        let cursor = $('<span class="typing-cursor">|</span>');
        if (el.find('.typing-cursor').length === 0) {
            el.append(cursor);
        } else {
            cursor = el.find('.typing-cursor');
        }
    
        function typeChar() {
            if (i < text.length) {
                cursor.before(text.charAt(i));
                i++;
                setTimeout(typeChar, speed);
            } else {
                cursor.remove(); // Remove cursor after done
            }
        }
    
        typeChar();
    }
});
