document.addEventListener("DOMContentLoaded", () => {
  // create a new WebSocket object.
  var socket = new WebSocket("ws://localhost:8000/ws");
  socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    if (data.username != uname) {
      appendMessage(data.username, "left", data.message);
    }
  };

  const msgerForm = get(".msger-inputarea");
  const msgerInput = get(".msger-input");
  const msgerChat = get(".msger-chat");

  //   const PERSON_NAME = "Sajad";

  msgerForm.addEventListener("submit", (event) => {
    event.preventDefault();
    console.log("hello");
    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage(uname, "right", msgText);
    // find the token in the cookie
    for (let i = 0; i < document.cookie.split(";").length; i++) {
      if (document.cookie.split(";")[i].split("=")[0] == "token") {
        var token = document.cookie.split(";")[i].split("=")[1];
      }
    }
    socket.send(
      JSON.stringify({
        message: msgText,
        username: uname,
        token: token,
      })
    );

    msgerInput.value = "";
  });

  function appendMessage(name, side, text) {
    //   Simple solution for small apps
    const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }

  // Utils
  function get(selector, root = document) {
    return root.querySelector(selector);
  }

  function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
  }

  function random(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
  }
});
