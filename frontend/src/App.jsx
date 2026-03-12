import { useState } from "react";
import Login from "./login";
import Dashboard from "./dashboard";

function App() {

  const [token,setToken] = useState(
    localStorage.getItem("token")
  );

  return (
    <div>
      {!token
        ? <Login setToken={setToken}/>
        : <Dashboard token={token}/>
      }
    </div>
  );
}

export default App;