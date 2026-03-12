import { useState } from "react";
import API from "./api";
import "./App.css";

function Login({ setToken }) {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await API.post("/login", { email, password });

      setToken(res.data.token);
      localStorage.setItem("token", res.data.token);

    } catch (err) {
        console.error("Login error:", err.response?.data || err.message);
        alert("Invalid email or password");
    }
  };

  // ENTER KEY SUPPORT
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      login();
    }
  };

  return (
    <div className="login-container">

      <h2>Student Portal</h2>

      <input
        placeholder="Email"
        autoFocus
        onChange={(e) => setEmail(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <button onClick={login}>Login</button>

    </div>
  );
}

export default Login;