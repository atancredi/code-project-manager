import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';

import './projects.css';

const tagColors = [
    "rgb(255, 228, 225)",
    "rgb(255, 224, 178)",
    "rgb(255, 248, 225)",
    "rgb(204, 255, 204)",
    "rgb(222, 238, 222)",
    "rgb(227, 242, 253)",
    "rgb(179, 229, 252)",
    "rgb(232, 234, 246)",
    "rgb(225, 213, 231)",
    "rgb(255, 229, 217)",
    "rgb(245, 245, 220)",
    "rgb(220, 220, 220)"
]

const App = () => {

    const [projects, setProjects] = useState([])
    const [categories, setCategories] = useState<string[][]>([])
    const getProjects = async () => {
        try {
            const response = await axios.get('/projects');
            setProjects(response.data);
            
            // get categories
            let cat = (response.data as any[]).map((x: any) => (x["tags"] as string[])).flat().filter((v,i,a) => a.indexOf(v) == i);
            console.log("fetched categories", cat)
            setCategories(cat.map((v,i) => ([v, tagColors[i]])))

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
    useEffect(()=>{
        console.log("set categories", categories)
    }, [categories])

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
            <div className='projects-container'>
            {projects.map((p, i) => (
                <div className='projects-item' key={p['name'] + i}>
                    <div className='projects-item-content'>
                        <div>
                            <button onClick={() => runProject(p['id'])}>{p['name']}</button>
                        </div>
                        <div className='projects-tags'>
                            {(p['tags'] as string[]).map((t, j) => (
                                <span key={t+j} style={{background: categories.find(v=>v[0]==t)?.[1] || "white"}}>{t}</span>
                            ))}
                        </div>
                    </div>
                    <div></div>
                </div>
            ))}
            </div>
        </div>
    );
};

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);