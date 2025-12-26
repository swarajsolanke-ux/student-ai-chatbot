async function send() {
  const msg = document.getElementById("msg").value;
  document.getElementById("chat").innerHTML += `<div>User: ${msg}</div>`;

  const res = await fetch("http://localhost:8000/chat", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ user_id:1, message:msg })
  });

  const data = await res.json();
  document.getElementById("chat").innerHTML += `<div>Bot: ${data.reply}</div>`;
}
