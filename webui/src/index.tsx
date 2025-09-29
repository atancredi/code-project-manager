import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios'; // Example package

const App = () => {

    const [projects, setProjects] = useState([])
    const getProjects = async () => {
        try {
            const response = await axios.get('/projects');
            setProjects(response.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };
    useEffect(() => {
        getProjects()
    }, [])
    useEffect(()=>{
        console.log("set projects", projects)
    }, [projects])

    const runProject = async (id: number) => {
        try {
            const response = await axios.get('/projects/'+id);
            console.log("started project", id)
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    return (
        <div>
            {projects.map((p, i) => (
                <div key={p['name'] + i}>
                    <button onClick={() => runProject(p['id'])}>{p['name']}</button> ({p['tags']})
                </div>
            ))}
        </div>
    );
};

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);