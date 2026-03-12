import { useEffect, useState } from "react";
import API from "./api";
import "./App.css";

function Dashboard({ token }) {

  const [students,setStudents] = useState([]);

  useEffect(()=>{

    const getStudents = async () => {

      const res = await API.get("/students",{
        headers:{
          Authorization:`Bearer ${token}`
        }
      });

      setStudents(res.data);
    };

    getStudents();

  },[token]);

  return (
    <div className="students-container">

      <h2>Students</h2>

      {students.map((s)=>(
        <div className="student" key={s._id}>
          <strong>{s.name}</strong>
          <br/>
          Course: {s.course}
        </div>
      ))}

    </div>
  );
}

export default Dashboard;