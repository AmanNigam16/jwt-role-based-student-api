import { useState } from "react";
import API from "./api";
import "./App.css";

function Login({ setToken }) {

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const login = async () => {
    const res = await API.post("/login",{email,password});
    setToken(res.data.token);
    localStorage.setItem("token",res.data.token);
  };

  return (
    <div className="login-container">

      <h2>Student Portal</h2>

      <input
        placeholder="Email"
        onChange={(e)=>setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>setPassword(e.target.value)}
      />

      <button onClick={login}>Login</button>

    </div>
  );
}

export default Login;