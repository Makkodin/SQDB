import React, { useState, useEffect } from "react";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Input } from 'semantic-ui-react'

function Projects() {

    // Блок отрисовки
    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ projects, setProjects ] = useState(null);

    // Блок поиска

    const [ filteredResults, setFilteredResults] = useState();

    // Подгрузка данных по именам проектов из flask
    useEffect(() => {
        fetch(`/projects`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setProjects(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, []);// eslint-disable-line react-hooks/exhaustive-deps
    
    
    const searchItems = (searchValue) => {

        if (searchValue) {
            const filterProjects = projects.filter((item) => {
                return Object.values(item).join('').toLowerCase().includes(searchValue.toLowerCase())
            })
            setFilteredResults(filterProjects)
        }
        else {setFilteredResults(projects)}   
    }

    //console.log(projects) 
    console.log(filteredResults) 

    // Отрисовка блоков
    let body = <></>;
    let head = <></>;
    let search = <></>;

    if (error) {
        return <div>Ошибка: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Загрузка...</div>;
    } else {
        head = (
            <thead>
                <tr>
                    <th>№</th>
                    <th>Проект</th>
                </tr>
            </thead>
        );
        
        
        body = (
            <tbody>
                {projects.map((prj, index) => {
                return (
                    <tr key={prj}>
                    <th>{index + 1}</th>
                    <th>
                        <Link to={`/projects/${prj}`}>{prj}</Link>
                    </th>
                    </tr>
                );
                })}
            </tbody>
        );

        search = (     
            <Input icon="search" placeholder='Поиск...' type="text" onChange={(e) => searchItems(e.target.value)}/>
        );
    }

    return (
        <><hr/>
        <Card className="Project-search">
        <b>Проекты</b><br/><br/>  
        Поиск по проектам:<br/>
        {search}
        <br/>
        </Card>    
        <hr/>


        <Card className="Project-names">
        <Table bordered hover >
            {head}
            {body}
        </Table>
        </Card>

        <hr/>
        </>
    );
}
export default Projects;
